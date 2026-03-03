import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Volatility Adjustment", layout="wide")

st.title("🛡️ Ajustement pour Volatilité (Volatility Adjustment)")
st.subheader("Mécanisme contracyclique de Solvabilité II")

st.markdown(r"""
Le **Volatility Adjustment (VA)** est une mesure du paquet "Garanties Long Terme" (LTG) de Solvabilité II. 
Il vise à éviter qu'une volatilité artificielle des spreads de crédit (non liée à un risque de défaut réel) 
ne dégrade excessivement le ratio de solvabilité des assureurs.

**Formule simplifiée :**
$$ VA = 65\% \times (Spread_{Portefeuille} - Spread_{Fondamental} - Correction_{Risque}) $$
""")

st.divider()

# --- PARAMÈTRES ---
st.header("Paramètres du Portefeuille")

col_p1, col_p2 = st.columns(2)

with col_p1:
    spread_market = st.slider("Spread de Crédit du Portefeuille (bps)", 0, 500, 150, step=10)
    fundamental_spread = st.slider("Spread Fondamental (bps)", 0, 100, 30, step=5, help="Partie du spread liée au risque de défaut réel (long terme)")

with col_p2:
    risk_correction = st.slider("Correction de Risque (bps)", 0, 100, 20, step=5)
    va_ratio = st.slider("Ratio d'application", 0.0, 1.0, 0.65, help="Standard S2 = 65%")

# --- CALCUL DU VA ---
# Calcul en points de base puis conversion en %
spread_net = max(0, spread_market - fundamental_spread - risk_correction)
va_value_bps = va_ratio * spread_net
va_value_pct = va_value_bps / 10000.0

# Affichage des KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Spread de Marché", f"{spread_market} bps")
col2.metric("Spread Ajusté (Net)", f"{spread_net} bps", help="Spread Market - FS - RC")
col3.metric("Volatility Adjustment (VA)", f"{va_value_bps:.1f} bps", delta=f"+{va_value_bps:.1f} bps")

# Visualisation de la décomposition
fig_decomp = go.Figure(data=[
    go.Bar(name='Spread Fondamental', x=['Décomposition du Spread'], y=[fundamental_spread], marker_color='gray'),
    go.Bar(name='Correction Risque', x=['Décomposition du Spread'], y=[risk_correction], marker_color='orange'),
    go.Bar(name='Volatility Adjustment (Absorbé)', x=['Décomposition du Spread'], y=[va_value_bps], marker_color='green'),
    go.Bar(name='Reste à charge (Impact Bilan)', x=['Décomposition du Spread'], y=[spread_net - va_value_bps], marker_color='red')
])
fig_decomp.update_layout(barmode='stack', title="Mécanisme d'absorption du Spread", yaxis_title="Points de base (bps)", height=300)
st.plotly_chart(fig_decomp, use_container_width=True)

st.divider()

# --- IMPACT SUR LA COURBE ---
st.header("1. Impact sur la Courbe des Taux Sans Risque")

# Construction de la courbe (taux swap théorique plat pour l'exemple ou courbe simple)
t = np.linspace(1, 40, 40)
# Courbe de base (légèrement croissante pour le réalisme)
r_base = 0.02 + 0.01 * (1 - np.exp(-t/10)) 
r_va = r_base + va_value_pct

fig = go.Figure()
fig.add_trace(go.Scatter(x=t, y=r_base*100, name="Courbe EIOPA (Sans VA)", line=dict(color='red', dash='dot')))
fig.add_trace(go.Scatter(x=t, y=r_va*100, name="Courbe EIOPA + VA", line=dict(color='green', width=3)))

fig.update_layout(
    title="Déformation de la courbe des taux d'actualisation",
    xaxis_title="Maturité (Années)",
    yaxis_title="Taux (%)",
    template="plotly_white"
)
st.plotly_chart(fig, use_container_width=True)

# --- IMPACT BILANTIEL ---
st.header("2. Impact sur le Bilan (Sensibilité)")

st.markdown("""
L'ajout du VA augmente le taux d'actualisation, ce qui **diminue la valeur des passifs (Best Estimate)** 
et augmente donc les Fonds Propres (Own Funds).
""")

# Simulation simplifiée d'un passif
duration = st.slider("Duration moyenne du Passif (Années)", 5, 30, 15)
bel_initial = 1000 # Base 1000 M€

# Estimation impact : Delta BEL approx = - Duration * Delta Taux * BEL
delta_bel = - duration * va_value_pct * bel_initial

col_res1, col_res2 = st.columns(2)

with col_res1:
    st.info("📉 **Impact sur le Best Estimate**")
    st.metric("Variation du BEL", f"{delta_bel:.1f} M€", delta_color="inverse")
    st.caption(f"Pour un passif théorique de {bel_initial} M€")

with col_res2:
    st.success("💰 **Impact sur les Fonds Propres**")
    st.metric("Gain en Capital (Pre-Tax)", f"{-delta_bel:.1f} M€")
    st.caption("Le VA agit comme un coussin de capital en période de crise.")