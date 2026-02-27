import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

import streamlit as st

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

# Sidebar for parameters
st.sidebar.header("Paramètres du Modèle")
b0 = st.sidebar.slider("Beta 0 (Niveau Long Terme)", 0.0, 0.10, 0.04, step=0.005)
b1 = st.sidebar.slider("Beta 1 (Pente)", -0.10, 0.10, -0.02, step=0.005)
b2 = st.sidebar.slider("Beta 2 (Courbure)", -0.10, 0.10, 0.01, step=0.005)
tau = st.sidebar.slider("Tau (Facteur d'échelle)", 0.1, 10.0, 2.0)

# Curve calculation
t = np.linspace(0.1, 30, 100)
term1 = (1 - np.exp(-t/tau)) / (t/tau)
term2 = term1 - np.exp(-t/tau)
y = b0 + b1*term1 + b2*term2

# Interactive visualization with Plotly
fig = go.Figure()
fig.add_trace(go.Scatter(x=t, y=y, mode='lines', name='Courbe Nelson-Siegel', line=dict(color='#1f77b4', width=3)))
fig.update_layout(title="Structure par Terme des Taux d'Intérêt", xaxis_title="Maturité (Années)", yaxis_title="Taux", template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

st.info("""
**Note :** Le modèle Nelson-Siegel est une approche parcimonieuse qui décrit la courbe des taux 
à l'aide de quatre paramètres clés, reflétant les anticipations du marché en matière d'inflation, de croissance et de liquidité.
""")

# --- PARAMETERS INTERPRETATION ---
st.markdown("### 2. Décomposition des Facteurs")
col_a, col_b = st.columns(2)

with col_a:
    st.markdown(f"""
    **$\\beta_0$ - Le Niveau (Taux Long Terme) :** Représente la valeur du taux lorsque la maturité tend vers l'infini. 
    Un changement de $\\beta_0$ indique un déplacement parallèle de la courbe.

    **$\\beta_1$ - La Pente (Décroissance Court Terme) :** Détermine la vitesse à laquelle la courbe atteint son niveau à long terme. 
    Un $\\beta_1$ négatif signifie généralement une courbe normale ascendante.
    """)

with col_b:
    st.markdown(f"""
    **$\\beta_2$ - La Courbure (Bosse Moyen Terme) :** Capture la 'bosse' spécifique dans le secteur 2 à 5 ans. 
    C'est critique pour la valorisation des passifs d'assurance à moyen terme.

    **$\\tau$ - Le Facteur d'Échelle :** Spécifie la maturité à laquelle le chargement sur la courbure est maximisé.
    """)

# --- RISK MANAGEMENT INSIGHTS ---
st.markdown("---")
st.markdown("### 3. Perspectives de Gestion des Risques")

st.write("""
Du point de vue de gestion des risques, le suivi de ces paramètres permet :
1. **Analyse de Scénarios :** Évaluer l'impact des "Twists" (changements de pente) et des "Butterflies" (changements de courbure) sur la Valeur Intrinsèque Nette.
2. **Stress Testing :** Quantifier la sensibilité du bilan Solvabilité II aux déplacements non parallèles.
3. **Pilotage ALM :** Ajuster l'écart de duration (gap) entre l'actif et le passif.
""")



