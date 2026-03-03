import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import norm

st.set_page_config(page_title="Modèles Risque de Marché", layout="wide")

st.title("📉 Modèles de Risque de Marché (Trading Book)")
st.subheader("De Bâle II.5 à FRTB : VaR, SVaR, IRC, CRM")

st.markdown("""
Cette page détaille les mesures de risque de marché utilisées pour le calcul des exigences de fonds propres des banques pour leurs activités de marché (Trading Book).
Ces mesures ont été renforcées suite à la crise de 2008 (Bâle 2.5) et évoluent avec la **Fundamental Review of the Trading Book (FRTB)**.
""")

st.divider()

# --- 1. VaR & Stressed VaR ---
st.header("1. Value-at-Risk (VaR) & Stressed VaR (SVaR)")

col1, col2 = st.columns(2)

with col1:
    st.info("### 📊 Value-at-Risk (VaR)")
    st.markdown("""
    La perte maximale potentielle sur un horizon donné (ex: 10 jours) avec un niveau de confiance donné (ex: 99%).
    *   **Calibrage :** Sur les 12 derniers mois (période courante).
    *   **Limite :** Procyclique (la VaR est basse quand les marchés sont calmes).
    """)

with col2:
    st.warning("### ⚡ Stressed VaR (SVaR)")
    st.markdown("""
    Introduite par Bâle 2.5 pour corriger la procyclicité de la VaR.
    *   **Calibrage :** Sur une période de 12 mois de **stress financier significatif** (ex: 2008).
    *   **Objectif :** Assurer un niveau de capital plancher même en période calme.
    """)

# Visualisation Interactive
st.subheader("Simulation : VaR vs SVaR")

vol_current = st.slider("Volatilité Courante (VaR)", 5.0, 50.0, 15.0, 1.0) / 100
vol_stressed = st.slider("Volatilité Stressée (SVaR)", 5.0, 100.0, 40.0, 1.0) / 100
confidence = st.selectbox("Niveau de Confiance", [0.95, 0.99], index=1)
horizon_days = 10

# Calcul VaR Paramétrique (1M€ portfolio)
exposure = 1_000_000
z_score = norm.ppf(confidence)
var = exposure * vol_current * np.sqrt(horizon_days/252) * z_score
svar = exposure * vol_stressed * np.sqrt(horizon_days/252) * z_score

c1, c2 = st.columns(2)
c1.metric(f"VaR ({confidence:.0%}, 10j)", f"{var:,.0f} €")
c2.metric(f"SVaR ({confidence:.0%}, 10j)", f"{svar:,.0f} €", delta=f"Ratio SVaR/VaR : {svar/var:.1f}x", delta_color="inverse")

# Graphique Distributions
x = np.linspace(-exposure*0.2, exposure*0.2, 1000)
pdf_var = norm.pdf(x, 0, exposure * vol_current * np.sqrt(horizon_days/252))
pdf_svar = norm.pdf(x, 0, exposure * vol_stressed * np.sqrt(horizon_days/252))

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=pdf_var, name="Distribution Courante (VaR)", fill='tozeroy', line=dict(color='blue')))
fig.add_trace(go.Scatter(x=x, y=pdf_svar, name="Distribution Stressée (SVaR)", fill='tozeroy', line=dict(color='red'), opacity=0.5))
fig.add_vline(x=-var, line_dash="dash", line_color="blue", annotation_text="VaR")
fig.add_vline(x=-svar, line_dash="dash", line_color="red", annotation_text="SVaR")
fig.update_layout(title="Distributions des P&L (VaR vs SVaR)", xaxis_title="P&L (€)", yaxis_title="Densité")
st.plotly_chart(fig, use_container_width=True)

st.divider()

# --- 2. IRC & CRM ---
st.header("2. Risques de Crédit Spécifiques (Bâle 2.5)")
st.markdown("Mesures additives pour capturer les risques mal couverts par la VaR sur les produits de crédit.")

col_irc, col_crm = st.columns(2)

with col_irc:
    st.error("### 🧱 Incremental Risk Charge (IRC)")
    st.write("""
    Capital pour couvrir les risques de **défaut** et de **migration de notation** (downgrade) sur les produits non titrisés (Obligations, CDS).
    *   **Horizon :** 1 an (liquidité constante).
    *   **Confiance :** 99.9%.
    *   **Pourquoi ?** La VaR (10 jours) ne capture pas le risque de saut (Jump-to-Default).
    """)

with col_crm:
    st.error("### 🕸️ Comprehensive Risk Measure (CRM)")
    st.write("""
    Mesure spécifique pour le **portefeuille de trading de corrélation** (ex: CDO tranches).
    *   Capture les risques de corrélation, de base, et de recouvrement.
    *   Remplace l'IRC pour ces produits complexes.
    """)

st.divider()

# --- 3. FUTUR : FRTB ---
st.header("3. L'avenir : FRTB (Fundamental Review of the Trading Book)")
st.markdown("""
La réforme FRTB remplace ces mesures par une approche plus cohérente.
""")

st.success("""
*   **VaR & SVaR** $\\rightarrow$ Remplacées par l'**Expected Shortfall (ES)** calibré sur une période de stress.
    *   *Avantage :* Capture mieux le risque de queue (Tail Risk) que la VaR.
*   **IRC & CRM** $\\rightarrow$ Remplacés par le **DRC (Default Risk Charge)**.
    *   Capitalisation explicite du risque de saut au défaut (Jump-to-Default).
""")