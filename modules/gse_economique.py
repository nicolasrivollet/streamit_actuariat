import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Générateur de Scénarios Économiques", layout="wide")

st.title("🎲 Générateur de Scénarios Économiques (GSE)")
st.subheader("Modélisation stochastique des actifs financiers")

st.markdown("""
Le **GSE (Economic Scenario Generator)** est le moteur de calcul des modèles internes et de la valorisation des options et garanties financières (TVOG).
Il permet de projeter des milliers de trajectoires possibles pour les facteurs de risque (Taux, Actions, Inflation) afin de capturer la distribution complète des résultats futurs.

On distingue deux mondes :
*   **Risk Neutral (RN) :** Pour la valorisation (Market Consistent). La moyenne des scénarios doit redonner le prix de marché actuel.
*   **Real World (RW) :** Pour la projection des risques réels et du P&L (ORSA). Inclut les primes de risque.
""")

st.divider()

# --- 1. PARAMÈTRES DE SIMULATION ---
st.header("1. Paramètres du Modèle (Black-Scholes)")

col1, col2 = st.columns(2)

with col1:
    S0 = st.number_input("Valeur Initiale de l'Indice (S0)", value=100.0)
    mu = st.slider("Drift (Tendance annuelle) %", -10.0, 20.0, 5.0, 0.5) / 100
    sigma = st.slider("Volatilité (Sigma) %", 5.0, 50.0, 20.0, 1.0) / 100

with col2:
    T = st.slider("Horizon de projection (Années)", 1, 40, 10)
    n_sim = st.slider("Nombre de simulations", 10, 1000, 100)
    dt = 1/12 # Pas mensuel

# --- 2. MOTEUR DE SIMULATION ---
# Modèle Black-Scholes : dS = S * (mu*dt + sigma*dW)
# Solution exacte : S(t) = S0 * exp((mu - 0.5*sigma^2)*t + sigma*W(t))

n_steps = int(T / dt)
time_grid = np.linspace(0, T, n_steps + 1)

# Génération des mouvements browniens
np.random.seed(42)
Z = np.random.normal(0, 1, (n_sim, n_steps))
W = np.cumsum(Z, axis=1) * np.sqrt(dt)
# Ajout de 0 au début pour W(0)=0
W = np.hstack([np.zeros((n_sim, 1)), W])

# Calcul des trajectoires
# S_t = S0 * exp((mu - 0.5*sigma^2)*t + sigma*W_t)
drift_term = (mu - 0.5 * sigma**2) * time_grid
diffusion_term = sigma * W
S = S0 * np.exp(drift_term + diffusion_term)

# --- 3. VISUALISATION ---
st.header("2. Visualisation des Trajectoires (Spaghetti Plot)")

fig = go.Figure()

# Afficher un sous-ensemble de trajectoires pour ne pas surcharger le graph
n_display = min(n_sim, 50)
for i in range(n_display):
    fig.add_trace(go.Scatter(x=time_grid, y=S[i], mode='lines', line=dict(width=1, color='rgba(31, 119, 180, 0.3)'), showlegend=False))

# Moyenne
mean_path = np.mean(S, axis=0)
fig.add_trace(go.Scatter(x=time_grid, y=mean_path, mode='lines', name='Moyenne', line=dict(width=3, color='red')))

# Percentiles
p05 = np.percentile(S, 5, axis=0)
p95 = np.percentile(S, 95, axis=0)
fig.add_trace(go.Scatter(x=time_grid, y=p95, mode='lines', name='95e percentile', line=dict(width=2, dash='dash', color='green')))
fig.add_trace(go.Scatter(x=time_grid, y=p05, mode='lines', name='5e percentile', line=dict(width=2, dash='dash', color='green')))

fig.update_layout(title=f"Projection de {n_sim} scénarios sur {T} ans", xaxis_title="Années", yaxis_title="Valeur de l'Indice")
st.plotly_chart(fig, use_container_width=True)

# --- 4. DISTRIBUTION TERMINALE ---
st.header("3. Distribution à Maturité")

final_values = S[:, -1]
ret_annuel = (final_values / S0)**(1/T) - 1

col_res1, col_res2 = st.columns(2)

with col_res1:
    fig_hist = go.Figure(data=[go.Histogram(x=final_values, nbinsx=30, marker_color='#1f77b4', opacity=0.7)])
    fig_hist.update_layout(title=f"Distribution des valeurs finales à T={T} ans", xaxis_title="Valeur Finale", yaxis_title="Fréquence")
    st.plotly_chart(fig_hist, use_container_width=True)

with col_res2:
    st.subheader("Statistiques")
    st.metric("Moyenne Finale", f"{np.mean(final_values):.2f}")
    st.metric("Volatilité observée (an)", f"{np.std(ret_annuel)*100:.2f}%")
    st.metric("VaR 99.5% (Perte)", f"{S0 - np.percentile(final_values, 0.5):.2f}", delta="Capital requis", delta_color="inverse")

st.info("""
**Note Technique :** 
Dans un cadre **Risk Neutral**, le drift $\mu$ serait égal au taux sans risque $r$. 
Ici, nous sommes dans une simulation **Real World** où $\mu$ inclut une prime de risque actions.
""")