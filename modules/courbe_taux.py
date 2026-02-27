import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# --- HEADER SECTION ---
st.title("Modélisation de la Courbe des Taux")
st.subheader("Le Modèle Nelson-Siegel")

st.markdown("""
Ce module démontre la modélisation paramétrique de la Structure par Terme des Taux d'Intérêt (TSIR). 
La maîtrise de la dynamique de la courbe des taux est essentielle pour la Gestion Actif-Passif (ALM), 
les exigences de capital de solvabilité réglementaire (SCR) et l'allocation stratégique d'actifs.
""")

# --- MATHEMATICAL FOUNDATION ---
st.markdown("### 1. Cadre Mathématique")
st.latex(r"""
y(t) = \beta_0 + \beta_1 \left( \frac{1 - e^{-t/\tau}}{t/\tau} \right) + \beta_2 \left( \frac{1 - e^{-t/\tau}}{t/\tau} - e^{-t/\tau} \right)
""")

st.divider()

# --- PARAMETERS IN THE MAIN PAGE ---
st.markdown("### 2. Simulateur de Paramètres")
st.write("Ajustez les curseurs pour observer les déformations de la courbe en temps réel.")

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

st.info("""
**Note :** Le modèle Nelson-Siegel est une approche parcimonieuse qui décrit la courbe des taux 
à l'aide de quatre paramètres clés, reflétant les anticipations du marché en matière d'inflation, de croissance et de liquidité.
""")



# --- PARAMETERS INTERPRETATION ---
st.markdown("### 3. Décomposition des Facteurs")
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

# --- RISK MANAGEMENT INSIGHTS ---
st.divider()
st.markdown("### 4. Perspectives de Gestion des Risques")

st.write("""
Le pilotage de ces paramètres permet de quantifier :
1. **Analyse de Scénarios :** Impact des "Twists" et "Butterflies" sur la valeur actuelle.
2. **Stress Testing :** Sensibilité du bilan aux chocs non-parallèles.
3. **Optimisation :** Ajustement du gap de duration actif-passif.
""")