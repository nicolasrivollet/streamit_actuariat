import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.optimize import minimize

# --- HEADER SECTION ---
st.title("Modélisation de la Courbe des Taux")
st.subheader("Le Modèle Nelson-Siegel")

st.markdown("""
Ce module démontre la modélisation paramétrique de la Structure par Terme des Taux d'Intérêt (TSIR). 
La maîtrise de la dynamique de la courbe des taux est essentielle pour la Gestion Actif-Passif (ALM), 
les exigences de capital de solvabilité réglementaire (SCR) et l'allocation stratégique d'actifs.

**Pourquoi Nelson-Siegel ?**
C'est le modèle standard utilisé par de nombreuses banques centrales et départements de risques. 
Il permet de résumer une courbe de taux complexe (des centaines de points) en seulement **4 paramètres** interprétables économiquement. Contrairement à une interpolation linéaire, il garantit une courbe lisse et continue.
""")

# --- MATHEMATICAL FOUNDATION ---
st.markdown("### 1. Cadre Mathématique")
st.latex(r"""
y(t) = \beta_0 + \beta_1 \left( \frac{1 - e^{-t/\tau}}{t/\tau} \right) + \beta_2 \left( \frac{1 - e^{-t/\tau}}{t/\tau} - e^{-t/\tau} \right)
""")

# --- PARAMETERS INTERPRETATION ---
st.markdown("### 3. Décomposition des Facteurs")
st.write("Chaque paramètre joue un rôle précis dans la forme de la courbe :")

col_a, col_b = st.columns(2)

with col_a:
    st.markdown(f"""
    **$\\beta_0$ - Le Niveau :** Représente la valeur asymptotique. 
    Un changement de $\\beta_0$ indique un déplacement parallèle.

    **$\\beta_1$ - La Pente :** Détermine la vitesse de convergence. 
    Un $\\beta_1$ négatif signifie une courbe normale (ascendante).
    """)

with col_b:
    st.markdown(f"""
    **$\\beta_2$ - La Courbure :** Capture la 'bosse' dans le secteur 2-5 ans. 
    Crucial pour l'ALM sur les passifs de durée moyenne.

    **$\\tau$ - Le Facteur d'Échelle :** Positionne le sommet de la courbure sur l'axe du temps.
    """)


st.divider()

# --- PARAMETERS IN THE MAIN PAGE ---
st.markdown("### 2. Simulateur de Paramètres")
st.info("**Expérimentation :** Ajustez les curseurs pour observer comment $\\beta_1$ fait pivoter la courbe (Pente) et comment $\\beta_2$ crée une bosse (Courbure).")

# Organisation des sliders en colonnes pour gagner de l'espace
col_param1, col_param2 = st.columns(2)

with col_param1:
    b0 = st.slider("Beta 0 (Niveau Long Terme)", 0.0, 0.10, 0.04, step=0.005)
    b1 = st.slider("Beta 1 (Pente)", -0.10, 0.10, -0.02, step=0.005)

with col_param2:
    b2 = st.slider("Beta 2 (Courbure)", -0.10, 0.10, 0.01, step=0.005)
    tau = st.slider("Tau (Facteur d'échelle)", 0.1, 10.0, 2.0)

# --- CALCULATIONS ---
t = np.linspace(0.1, 30, 100)
term1 = (1 - np.exp(-t/tau)) / (t/tau)
term2 = term1 - np.exp(-t/tau)
y = b0 + b1*term1 + b2*term2

# --- VISUALIZATION ---
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=t, 
    y=y * 100, # Conversion en % pour plus de lisibilité
    mode='lines', 
    name='Courbe Nelson-Siegel', 
    line=dict(color='#1f77b4', width=4)
))

fig.update_layout(
    title="Structure par Terme des Taux d'Intérêt (Visualisation en %)",
    xaxis_title="Maturité (Années)",
    yaxis_title="Taux (%)",
    template="plotly_white",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)



# --- CALIBRATION SECTION ---
st.divider()
st.markdown("### 5. Calibration Automatique (Fitting)")
st.markdown("""
Dans la pratique, l'actuaire ne "choisit" pas les paramètres au hasard. Il cherche les paramètres qui permettent à la courbe théorique de passer le plus près possible des taux réellement observés sur le marché (OAT, Swaps).

**Comment ça marche ?**
L'algorithme ci-dessous utilise une méthode d'optimisation (Nelder-Mead) pour minimiser la somme des écarts au carré (MSE) entre le modèle et les points de marché saisis. C'est cette étape qui permet de passer des cotations de marché (discrètes) à une courbe continue utilisable pour valoriser n'importe quel flux financier.
""")

col_calib1, col_calib2 = st.columns([1, 2])

with col_calib1:
    st.markdown("**Données de Marché (Input)**")
    # Données par défaut
    input_data = pd.DataFrame({
        "Maturité (Ans)": [1, 2, 5, 10, 20],
        "Taux (%)": [2.50, 2.75, 3.10, 3.45, 3.85]
    })
    # Éditeur interactif
    edited_df = st.data_editor(input_data, num_rows="dynamic", hide_index=True)


with col_calib2:
    # Préparation des données
    t_obs = edited_df["Maturité (Ans)"].values
    y_obs = edited_df["Taux (%)"].values / 100
    
    # Fonction Nelson-Siegel pour l'optimiseur
    def ns_curve(t, params):
        b0, b1, b2, tau = params
        term1 = (1 - np.exp(-t/tau)) / (t/tau)
        term2 = term1 - np.exp(-t/tau)
        return b0 + b1*term1 + b2*term2
        
    # Fonction Objectif (Somme des Carrés des Écarts)
    def objective(params):
        # Contrainte : Tau doit être strictement positif pour éviter la division par zéro
        if params[3] <= 0.1: return 1e6
        y_pred = ns_curve(t_obs, params)
        return np.sum((y_pred - y_obs)**2)
        
    # Optimisation (Nelder-Mead est robuste pour ce type de problème non-linéaire)
    x0 = [0.03, -0.01, 0.0, 2.0] # Initial guess
    res = minimize(objective, x0, method='Nelder-Mead')
    
    # Résultats
    b0_opt, b1_opt, b2_opt, tau_opt = res.x
    

    
    
    # Visualisation Comparative
    t_plot = np.linspace(0.1, max(t_obs)+5, 100)
    y_fit = ns_curve(t_plot, res.x)
    
    fig_fit = go.Figure()
    fig_fit.add_trace(go.Scatter(x=t_plot, y=y_fit*100, name="Courbe Calibrée (NS)", line=dict(color='green', width=3)))
    fig_fit.add_trace(go.Scatter(x=t_obs, y=y_obs*100, mode='markers', name="Points Marché", marker=dict(color='red', size=12, symbol='x')))
    fig_fit.update_layout(title="Résultat du Fitting", xaxis_title="Maturité (Années)", yaxis_title="Taux (%)", template="plotly_white")
    st.plotly_chart(fig_fit, use_container_width=True)

    # Affichage des paramètres calibrés
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Beta 0 (Niveau)", f"{b0_opt:.4f}")
    c2.metric("Beta 1 (Pente)", f"{b1_opt:.4f}")
    c3.metric("Beta 2 (Courbure)", f"{b2_opt:.4f}")
    c4.metric("Tau", f"{tau_opt:.4f}")

    st.info(f"Calibration automatique (MSE : {res.fun:.2e})")
