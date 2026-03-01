import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Processus ORSA", layout="wide")

st.title("🔄 Processus ORSA (Own Risk and Solvency Assessment)")
st.subheader("L'évaluation interne des risques et de la solvabilité (Pilier 2)")

st.markdown("""
L'**ORSA** est le cœur du Pilier 2 de Solvabilité II. C'est un processus continu (et non un simple rapport annuel) qui permet à l'assureur d'évaluer ses besoins globaux de solvabilité en fonction de son profil de risque spécifique, de sa tolérance au risque et de sa stratégie commerciale.

Contrairement au Pilier 1 (Formule Standard) qui est une "photo" à un instant T, l'ORSA est une **"vidéo" prospective** sur l'horizon du plan stratégique (3 à 5 ans).
""")

st.divider()

# --- 1. LE CYCLE ORSA ---
st.header("1. Le Cycle ORSA")
st.markdown("L'ORSA connecte la stratégie, les risques et le capital.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.info("**1. Stratégie**\nDéfinition du Business Plan et de l'Appétence au Risque.")
with col2:
    st.warning("**2. Identification**\nCartographie des risques (y compris émergents et non modélisés).")
with col3:
    st.success("**3. Évaluation**\nCalcul du besoin de capital prospectif (Scénario Central + Stress).")
with col4:
    st.error("**4. Décision**\nValidation par le Conseil et intégration dans le pilotage.")

st.divider()

# --- 2. SCÉNARIOS ORSA ---
st.header("2. Projection et Scénarios de Stress")
st.markdown("""
L'assureur doit projeter sa solvabilité sur la durée du plan stratégique (ex: 5 ans).
Il doit tester la résilience de ce plan face à des chocs adverses (**Scénarios ORSA**).
""")

# Paramètres de simulation
years = np.arange(2024, 2029)
n_years = len(years)

# Scénario Central (Business Plan) - Hypothèse de croissance légère du ratio
base_ratio = np.linspace(200, 220, n_years) 

# Définition des chocs interactifs
st.subheader("Simulateur de Trajectoires de Solvabilité")

col_scen1, col_scen2 = st.columns([1, 2])

with col_scen1:
    st.markdown("**Paramétrage des Chocs**")
    
    # Scénario 1 : Financier
    st.write("📉 **Scénario Krach Financier**")
    shock_fin_year = st.selectbox("Année du choc", years, index=1)
    shock_fin_impact = st.slider("Impact sur le Ratio S2 (pts)", 10, 100, 40, help="Perte de solvabilité immédiate suite au krach.")
    
    # Scénario 2 : Inflation / Technique
    st.write("🔥 **Scénario Inflation / Dérapage**")
    trend_infl = st.slider("Érosion annuelle du ratio (pts/an)", 0, 20, 5, help="Baisse continue de la solvabilité due à l'inflation des coûts ou des sinistres.")

with col_scen2:
    # Calcul des trajectoires
    
    # 1. Trajectoire Krach (Choc ponctuel + récupération lente)
    ratio_krach = base_ratio.copy()
    idx_shock = np.where(years == shock_fin_year)[0][0]
    ratio_krach[idx_shock:] -= shock_fin_impact
    # Récupération progressive (5 pts par an après le choc)
    for i in range(idx_shock + 1, n_years):
        ratio_krach[i] += (i - idx_shock) * 5
        
    # 2. Trajectoire Inflation (Érosion continue)
    ratio_infl = base_ratio.copy()
    for i in range(n_years):
        ratio_infl[i] -= i * trend_infl

    # Visualisation
    fig = go.Figure()
    
    # Zones d'appétence au risque
    fig.add_hrect(y0=0, y1=100, fillcolor="red", opacity=0.1, line_width=0, annotation_text="Zone Critique (<100%)", annotation_position="bottom right")
    fig.add_hrect(y0=100, y1=140, fillcolor="orange", opacity=0.1, line_width=0, annotation_text="Zone de Tolérance", annotation_position="bottom right")
    fig.add_hrect(y0=140, y1=250, fillcolor="green", opacity=0.1, line_width=0, annotation_text="Zone Cible", annotation_position="top right")
    
    # Courbes
    fig.add_trace(go.Scatter(x=years, y=base_ratio, name="Scénario Central (BP)", line=dict(color='green', width=4)))
    fig.add_trace(go.Scatter(x=years, y=ratio_krach, name="Scénario Krach Financier", line=dict(color='blue', dash='dash')))
    fig.add_trace(go.Scatter(x=years, y=ratio_infl, name="Scénario Inflation Durable", line=dict(color='orange', dash='dot')))
    
    fig.update_layout(title="Projection du Ratio de Solvabilité (ORSA)", xaxis_title="Année", yaxis_title="Ratio S2 (%)", yaxis_range=[50, 250], hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

# --- 3. REVERSE STRESS TESTS ---
st.header("3. Reverse Stress Tests (Tests de Solvabilité Inverse)")
with st.expander("☠️ Comprendre le concept", expanded=True):
    st.write("""
    Au lieu de partir d'un choc plausible et de voir l'impact, on part de la "mort" de l'entreprise (Ratio < 100%) et on remonte le fil pour trouver quel scénario catastrophe pourrait causer cela.
    
    *   **Objectif :** Identifier les vulnérabilités cachées du modèle d'affaires.
    *   **Exemple :** Une pandémie mondiale combinée à un krach obligataire et une cyberattaque massive.
    """)