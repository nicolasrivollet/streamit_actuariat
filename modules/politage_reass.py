import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(page_title="Actuarial Strategy Dashboard", layout="wide")

st.title("📊 Pilotage Stratégique : Optimisation Solvabilité & Réassurance")
st.markdown("---")

# --- SIDEBAR : INPUTS STRATÉGIQUES ---
st.sidebar.header("Paramètres du Portefeuille")
prime_brute = st.sidebar.number_input("Primes Émises Brutes (M€)", value=100.0)
frais_gestion = st.sidebar.slider("Chargement de frais (%)", 5, 30, 15) / 100

st.sidebar.header("Structure de Réassurance (XL)")
priorite = st.sidebar.slider("Priorité (Rétention) (M€)", 0.5, 10.0, 2.0)
portee = st.sidebar.slider("Portée du Traité (M€)", 1.0, 50.0, 10.0)

# --- ENGINE : SIMULATION MONTE CARLO ---
@st.cache_data
def simulate_claims(n=10000):
    # Simulation d'une sinistralité avec queue de distribution (Lognormale)
    return np.random.lognormal(mean=0.5, sigma=0.8, size=n)

claims = simulate_claims()

# Application du traité XL
claims_net = np.where(claims > priorite, 
                      np.where(claims > priorite + portee, claims - portee, priorite), 
                      claims)

# --- CALCULS KPI ---
loss_ratio_brut = claims.mean() / (prime_brute / 10) # Simple proxy pour l'exercice
loss_ratio_net = claims_net.mean() / (prime_brute / 10)

# Estimation SCR Simplifiée (Impact sur les fonds propres)
scr_brut = 0.25 * prime_brute  # Proxy 25% des primes
scr_net = scr_brut * (claims_net.std() / claims.std()) # Réduction par la baisse de volatilité

# --- AFFICHAGE ---
col1, col2, col3 = st.columns(3)
col1.metric("Ratio Combiné Brut", f"{round(loss_ratio_brut * 100 + frais_gestion*100, 1)}%")
col2.metric("Économie SCR (Est.)", f"{round(scr_brut - scr_net, 2)} M€", delta_color="normal")
col3.metric("Ratio de Solvabilité", f"{round((40 / scr_net) * 100, 0)}%", delta="5%")

# Graphique de distribution
st.subheader("Analyse de la volatilité : Brut vs Net")
fig, ax = plt.subplots(figsize=(10, 4))
ax.hist(claims, bins=100, alpha=0.5, label="Sinistres Bruts", color="red")
ax.hist(claims_net, bins=100, alpha=0.5, label="Sinistres Nets (XL)", color="green")
ax.set_xlim(0, 15)
ax.legend()
st.pyplot(fig)