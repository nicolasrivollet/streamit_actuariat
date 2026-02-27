import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import smithwilson as sw

# --- INTERFACE UTILISATEUR ---

st.title("📏 Calculateur Smith-Wilson")
st.markdown("""
Cette page utilise la librairie industrielle **smithwilson** pour extrapoler la courbe des taux selon la réglementation **Solvabilité II**. 
Le modèle garantit une **interpolation exacte** des points de marché tout en convergeant vers l'UFR.
""")

st.divider()

# --- INPUTS ---
col_in1, col_in2 = st.columns([1, 2])

with col_in1:
    st.subheader("📊 Données de Marché")
    st.write("Modifiez les taux pour recalculer la courbe :")
    
    # Données par défaut (ex: Swap Rates ou OAT)
    df_market = pd.DataFrame({
        'Maturité': [1.0, 2.0, 5.0, 10.0, 20.0],
        'Taux (%)': [2.85, 2.95, 3.15, 3.40, 3.75]
    })
    edited_df = st.data_editor(df_market, num_rows="dynamic")
    
    st.subheader("⚙️ Paramètres EIOPA")
    # Valeur mise à jour pour 2026 : 3.30%
    ufr_val = st.slider("Ultimate Forward Rate (UFR) %", 2.0, 5.0, 3.30, step=0.05) / 100
    alpha_val = st.slider("Vitesse de Convergence (Alpha)", 0.05, 0.50, 0.1285, step=0.001)
    
    t_market = edited_df['Maturité'].values
    r_market = edited_df['Taux (%)'].values / 100
    llp = t_market.max()

with col_in2:
    st.subheader("📈 Visualisation de l'Extrapolation")
    
    # Définition de l'horizon de projection (ex: 80 ans)
    t_target = np.linspace(1, 80, 80) 
    
    try:
        # Appel à la librairie smithwilson
        # fit_smithwilson_rates retourne les taux pour t_target
        y_target = sw.fit_smithwilson_rates(
            rates_obs=r_market, 
            t_obs=t_market,
            t_target=t_target, 
            ufr=ufr_val, 
            alpha=alpha_val
        )
        
        fig = go.Figure()
        
        # Zone Liquide vs Extrapolation
        fig.add_vrect(x0=0, x1=llp, fillcolor="green", opacity=0.05, line_width=0, annotation_text="Zone Liquide")
        fig.add_vrect(x0=llp, x1=max(t_target), fillcolor="blue", opacity=0.05, line_width=0, annotation_text="Extrapolation")
        
        # Courbe Smith-Wilson
        fig.add_trace(go.Scatter(x=t_target, y=y_target*100, name="Courbe S-W", line=dict(color='#1E88E5', width=4)))
        
        # Points de Marché (Inputs)
        fig.add_trace(go.Scatter(x=t_market, y=r_market*100, name="Marché", mode='markers', marker=dict(color='red', size=10, symbol='diamond')))
        
        # Ligne UFR
        fig.add_hline(y=ufr_val*100, line_dash="dash", line_color="orange", annotation_text="Cible UFR")

        fig.update_layout(
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis_title="Maturité (Années)",
            yaxis_title="Taux Actuariel (%)",
            legend=dict(yanchor="bottom", y=0.01, xanchor="right", x=0.99),
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Erreur de calcul : {e}")

st.divider()

# --- ANALYSE DE ROBUSTESSE ---
st.header("🔬 Analyse de la Calibration")

check_col1, check_col2, check_col3 = st.columns(3)

with check_col1:
    # On vérifie l'interpolation sur les maturités d'origine
    y_check = sw.fit_smithwilson_rates(r_market, t_market, t_market, ufr_val, alpha_val)
    # On prend le point à 10 ans (si présent) ou le dernier point
    st.metric("Taux au LLP (Calculé)", f"{y_check[-1]*100:.4f}%")
    st.caption(f"Cible marché : {r_market[-1]*100:.4f}%")

with check_col2:
    st.metric(f"Convergence à {int(max(t_target))} ans", f"{y_target[-1]*100:.3f}%")
    st.caption(f"Cible UFR : {ufr_val*100:.2f}%")

with check_col3:
    st.metric("Dernier Point Liquide (LLP)", f"{llp} ans")
    st.caption("Début du raccordement.")

# --- FOOTER TECHNIQUE ---
with st.expander("📚 Détails méthodologiques (Librairie SmithWilson)"):
    st.write("""
    Cette implémentation utilise la librairie `smithwilson` pour automatiser la résolution du système matriciel.
    
    **Propriétés du modèle :**
    * **Interpolation exacte** : L'écart entre les taux observés et les taux ajustés est nul par construction (résolution de $W \zeta = m - \mu$).
    * **Continuité** : La courbe est de classe $C^1$ (dérivable), ce qui est crucial pour éviter les sauts de taux *forward*.
    * **Extrapolation** : Au-delà du LLP, la vitesse de convergence est pilotée par le paramètre Alpha.
    """)

st.caption("Implémentation via package smithwilson - Portfolio Actuariat 2026")