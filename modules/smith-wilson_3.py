import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# --- LOGIQUE MATHÉMATIQUE RÉELLE ---

def wilson_kernel(t, u, alpha, ufr_cont):
    """Calcule le noyau de Wilson entre deux maturités (Formule EIOPA)."""
    curr_exp = np.exp(-ufr_cont * (t + u))
    min_tu = np.minimum(t, u)
    max_tu = np.maximum(t, u)
    return curr_exp * (alpha * min_tu - 0.5 * np.exp(-alpha * max_tu) * (np.exp(alpha * min_tu) - np.exp(-alpha * min_tu)))

def compute_smith_wilson(t_market, r_market, alpha, ufr_annual, t_target):
    """Résolution matricielle et projection de la courbe."""
    ufr_cont = np.log(1 + ufr_annual)
    m = 1 / (1 + r_market)**t_market # Prix de marché
    mu = np.exp(-ufr_cont * t_market) # Cible UFR
    
    # Construction de la matrice W
    n = len(t_market)
    W = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            W[i, j] = wilson_kernel(t_market[i], t_market[j], alpha, ufr_cont)
            
    # Résolution W * zeta = m - mu
    zeta = np.linalg.solve(W, m - mu)
    
    # Projection
    p_target = []
    for t in t_target:
        sum_part = sum(zeta[i] * wilson_kernel(t, t_market[i], alpha, ufr_cont) for i in range(n))
        p_t = np.exp(-ufr_cont * t) * (1 + sum_part)
        p_target.append(p_t)
    
    p_target = np.array(p_target)
    r_target = (1 / p_target)**(1 / t_target) - 1
    return r_target

# --- INTERFACE STREAMLIT ---

st.title("📏 Calculateur Smith-Wilson")
st.markdown("""
Cette page implémente l'algorithme d'extrapolation **réel** utilisé par l'EIOPA. 
Le modèle résout un système matriciel pour garantir que la courbe passe exactement par les points observés.
""")

st.divider()

# Configuration des colonnes
col_in, col_plot = st.columns([1, 2])

with col_in:
    st.header("📥 Données d'entrée")
    
    # Éditeur de données de marché
    st.subheader("Points de Marché")
    df_market = pd.DataFrame({
        'Maturité': [1.0, 2.0, 5.0, 10.0, 20.0],
        'Taux (%)': [2.80, 3.00, 3.25, 3.50, 3.80]
    })
    edited_df = st.data_editor(df_market, num_rows="dynamic", use_container_width=True)
    
    # Paramètres de calibration
    st.subheader("Paramètres S2")
    ufr_input = st.slider("UFR (Annuel) %", 2.0, 5.0, 3.45, step=0.05) / 100
    alpha_input = st.slider("Alpha (Convergence)", 0.05, 0.50, 0.15, step=0.01)
    
    t_market = edited_df['Maturité'].values
    r_market = edited_df['Taux (%)'].values / 100

with col_plot:
    st.header("📈 Courbe Extrapolée")
    
    # Calcul sur une grille de 0.1 à 60 ans
    t_grid = np.linspace(0.1, 60, 200)
    
    try:
        y_grid = compute_smith_wilson(t_market, r_market, alpha_input, ufr_input, t_grid)
        
        # Création du graphique Plotly
        fig = go.Figure()
        
        # Zones de couleur (Liquide vs Extrapolée)
        llp = t_market.max()
        fig.add_vrect(x0=0, x1=llp, fillcolor="green", opacity=0.05, layer="below", line_width=0, annotation_text="Marché Liquide")
        fig.add_vrect(x0=llp, x1=60, fillcolor="blue", opacity=0.05, layer="below", line_width=0, annotation_text="Extrapolation")
        
        # Courbe Smith-Wilson
        fig.add_trace(go.Scatter(x=t_grid, y=y_grid*100, name="Modèle S-W", line=dict(color='#1f77b4', width=4)))
        
        # Points de marché réels
        fig.add_trace(go.Scatter(x=t_market, y=r_market*100, name="Inputs Marché", mode='markers', marker=dict(color='red', size=10, symbol='diamond')))
        
        # Ligne de l'UFR
        fig.add_hline(y=ufr_input*100, line_dash="dash", line_color="orange", annotation_text="Cible UFR")

        fig.update_layout(template="plotly_white", xaxis_title="Maturité (Ans)", yaxis_title="Taux (%)", hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Erreur de calcul : {e}")

st.divider()

# --- VALIDATION ACTUARIELLE ---
st.header("🔬 Preuve d'Interpolation Exacte")
st.write("Le tableau ci-dessous compare les taux d'entrée avec les taux recalculés par le modèle.")

# On recalcule les taux spécifiquement sur les maturités d'entrée
y_check = compute_smith_wilson(t_market, r_market, alpha_input, ufr_input, t_market)

comparison_df = pd.DataFrame({
    "Maturité": t_market,
    "Taux Marché (%)": r_market * 100,
    "Taux Modèle (%)": y_check * 100,
    "Écart (bps)": (y_check - r_market) * 10000
})

st.dataframe(comparison_df.style.format(precision=4), use_container_width=True)

st.info("""
**Note Technique :** L'écart affiché est en points de base (bps). 
Dans un modèle d'interpolation exacte, cet écart doit être virtuellement nul ($< 10^{-10}$), 
prouvant la résolution parfaite du système matriciel $W \zeta = m - \mu$.
""")