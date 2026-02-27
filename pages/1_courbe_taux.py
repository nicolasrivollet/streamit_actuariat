import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.title("Modélisation de la Courbe de Taux")
st.subheader("Modèle de Nelson-Siegel")

st.markdown(r"""
Le modèle de Nelson-Siegel permet de reconstruire la structure par terme des taux d'intérêt via la formule :
""")

st.latex(r"""
y(t) = \beta_0 + \beta_1 \left( \frac{1 - e^{-t/\tau}}{t/\tau} \right) + \beta_2 \left( \frac{1 - e^{-t/\tau}}{t/\tau} - e^{-t/\tau} \right)
""")

st.write("Où :")
col_a, col_b = st.columns(2)
with col_a:
    st.write("- $\\beta_0$ : Niveau (Long terme)")
    st.write("- $\\beta_1$ : Pente (Court terme)")
with col_b:
    st.write("- $\\beta_2$ : Courbure")
    st.write("- $\\tau$ : Facteur d'échelle")

# Barre latérale pour les paramètres
st.sidebar.header("Paramètres du Modèle")
b0 = st.sidebar.slider("Beta 0 (Niveau long terme)", 0.0, 0.10, 0.04, step=0.005)
b1 = st.sidebar.slider("Beta 1 (Pente)", -0.10, 0.10, -0.02, step=0.005)
b2 = st.sidebar.slider("Beta 2 (Courbure)", -0.10, 0.10, 0.01, step=0.005)
tau = st.sidebar.slider("Tau (Facteur d'échelle)", 0.1, 10.0, 2.0)

# Calcul de la courbe
t = np.linspace(0.1, 30, 100)
term1 = (1 - np.exp(-t/tau)) / (t/tau)
term2 = term1 - np.exp(-t/tau)
y = b0 + b1*term1 + b2*term2

# Visualisation interactive avec Plotly
fig = go.Figure()
fig.add_trace(go.Scatter(x=t, y=y, mode='lines', name='Courbe Nelson-Siegel', line=dict(color='#1f77b4', width=3)))
fig.update_layout(title="Structure par terme des taux d'intérêt", xaxis_title="Maturité (Années)", yaxis_title="Taux", template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

# Analyse de Risque - Vision Head of Risk
st.markdown("---")
st.write("### 🧠 Analyse Stratégique")
if b1 < 0:
    st.success("La courbe est **normale** (pente positive). Les anticipations économiques sont stables.")
else:
    st.error("La courbe est **inversée**. Attention : risque de récession ou tension de liquidité à court terme.")