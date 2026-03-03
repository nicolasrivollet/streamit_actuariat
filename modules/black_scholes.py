import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import norm

st.set_page_config(page_title="Modèle Black-Scholes", layout="wide")

st.title("📉 Modèle de Black-Scholes-Merton")
st.subheader("Valorisation d'Options Européennes & Calcul des Grecques")

st.markdown("""
Le modèle de **Black-Scholes** (1973) est la pierre angulaire de la finance quantitative. 
Il permet de calculer la valeur théorique d'une option européenne (Call ou Put) ne versant pas de dividendes, en fonction de plusieurs paramètres de marché.

$$ C(S, t) = S_t N(d_1) - K e^{-r(T-t)} N(d_2) $$
$$ P(S, t) = K e^{-r(T-t)} N(-d_2) - S_t N(-d_1) $$

Avec :
$$ d_1 = \\frac{\\ln(S_t/K) + (r + \\sigma^2/2)(T-t)}{\\sigma \\sqrt{T-t}} $$
$$ d_2 = d_1 - \\sigma \\sqrt{T-t} $$
""")

st.divider()

# --- 1. PARAMÈTRES ---
st.header("1. Paramètres de l'Option")

col1, col2, col3 = st.columns(3)

with col1:
    S = st.number_input("Prix du Sous-jacent (S)", value=100.0, step=1.0)
    K = st.number_input("Prix d'Exercice (Strike K)", value=100.0, step=1.0)

with col2:
    T = st.number_input("Maturité (Années)", value=1.0, step=0.1, min_value=0.01)
    r = st.number_input("Taux sans risque (r) %", value=5.0, step=0.1) / 100

with col3:
    sigma = st.slider("Volatilité (σ) %", 1.0, 100.0, 20.0, step=1.0) / 100
    opt_type = st.radio("Type d'Option", ["Call", "Put"])

# --- 2. MOTEUR DE CALCUL ---
def black_scholes(S, K, T, r, sigma, type="Call"):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if type == "Call":
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return price

def calculate_greeks(S, K, T, r, sigma, type="Call"):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if type == "Call":
        delta = norm.cdf(d1)
        rho = K * T * np.exp(-r * T) * norm.cdf(d2)
        theta = - (S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2)
    else:
        delta = norm.cdf(d1) - 1
        rho = -K * T * np.exp(-r * T) * norm.cdf(-d2)
        theta = - (S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * norm.cdf(-d2)

    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T)
    
    return {"Delta": delta, "Gamma": gamma, "Vega": vega / 100, "Theta": theta / 365, "Rho": rho / 100}

price = black_scholes(S, K, T, r, sigma, opt_type)
greeks = calculate_greeks(S, K, T, r, sigma, opt_type)

# --- 3. RÉSULTATS ---
st.header("2. Valorisation & Sensibilités (Grecques)")

c1, c2 = st.columns([1, 3])

with c1:
    st.metric(f"Prix du {opt_type}", f"{price:.2f} €")
    st.markdown("### Les Grecques")
    st.metric("Delta (Δ)", f"{greeks['Delta']:.3f}", help="Sensibilité au prix du sous-jacent")
    st.metric("Gamma (Γ)", f"{greeks['Gamma']:.3f}", help="Sensibilité du Delta au prix du sous-jacent (Convexité)")
    st.metric("Vega (ν)", f"{greeks['Vega']:.3f}", help="Sensibilité à la volatilité (pour 1%)")
    st.metric("Theta (Θ)", f"{greeks['Theta']:.3f}", help="Perte de valeur quotidienne (Time Decay)")
    st.metric("Rho (ρ)", f"{greeks['Rho']:.3f}", help="Sensibilité au taux d'intérêt (pour 1%)")

with c2:
    # Graphique : Prix vs Spot
    st.subheader("Analyse de Sensibilité : Prix vs Spot")
    
    spot_range = np.linspace(S * 0.5, S * 1.5, 100)
    prices = [black_scholes(s, K, T, r, sigma, opt_type) for s in spot_range]
    
    # Payoff à maturité
    if opt_type == "Call":
        payoff = np.maximum(spot_range - K, 0)
    else:
        payoff = np.maximum(K - spot_range, 0)
        
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=spot_range, y=prices, name=f"Prix {opt_type} (Black-Scholes)", line=dict(color='blue', width=3)))
    fig.add_trace(go.Scatter(x=spot_range, y=payoff, name="Payoff Intrinsèque (Maturité)", line=dict(color='black', dash='dash')))
    
    # Marquer le point actuel
    fig.add_trace(go.Scatter(x=[S], y=[price], mode='markers', name='Situation Actuelle', marker=dict(color='red', size=12)))
    
    fig.update_layout(xaxis_title="Prix du Sous-jacent (Spot)", yaxis_title="Prix de l'Option", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# --- 4. SURFACE DE VOLATILITÉ (OPTIONNEL) ---
st.header("3. Surface de Prix (Spot x Maturité)")
st.markdown("Visualisation 3D de l'évolution du prix de l'option en fonction du Spot et du Temps restant.")

spot_3d = np.linspace(S * 0.5, S * 1.5, 30)
time_3d = np.linspace(0.01, T, 30)
spot_grid, time_grid = np.meshgrid(spot_3d, time_3d)

# Vectorisation simple pour la grille
def bs_vectorized(s, t):
    return black_scholes(s, K, t, r, sigma, opt_type)

z_price = np.vectorize(bs_vectorized)(spot_grid, time_grid)

fig_3d = go.Figure(data=[go.Surface(z=z_price, x=spot_3d, y=time_3d, colorscale='Viridis')])
fig_3d.update_layout(scene=dict(
    xaxis_title='Spot',
    yaxis_title='Temps (Années)',
    zaxis_title='Prix Option'
), height=600)

st.plotly_chart(fig_3d, use_container_width=True)