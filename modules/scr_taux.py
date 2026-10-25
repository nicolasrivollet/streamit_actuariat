import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="SCR Taux - Formule Standard", layout="wide")

st.title("SCR Marché : Risque de Taux d'Intérêt")
st.subheader("Calcul selon la Formule Standard (Solvabilité II)")

st.markdown("""
Le **SCR Taux** (Interest Rate Risk) mesure le capital nécessaire pour faire face à une variation défavorable de la courbe des taux.
La réglementation impose de tester deux scénarios de stress sur la courbe des taux sans risque :

1.  **Choc UP (Hausse) :** Multiplication des taux par un facteur $(1 + s^{up}_t)$. Impacte négativement la valeur des obligations.
2.  **Choc DOWN (Baisse) :** Multiplication des taux par un facteur $(1 + s^{down}_t)$. Impacte négativement les assureurs ayant des passifs longs (augmentation du Best Estimate).

$$ SCR_{taux} = \max( \Delta NAV_{up}, \Delta NAV_{down}, 0 ) $$
""")

st.divider()

# --- 1. PARAMÈTRES ---
col_param1, col_param2 = st.columns(2)

with col_param1:
    st.header("1. Courbe Initiale")
    b0 = st.slider("Niveau (Beta 0)", 0.0, 0.10, 0.03, 0.005)
    b1 = st.slider("Pente (Beta 1)", -0.05, 0.05, 0.01, 0.005)
    tau = st.slider("Tau", 0.1, 5.0, 2.0)
    # On fixe b2 pour simplifier l'interface, ou on le met à 0
    b2 = 0.0

with col_param2:
    st.header("2. Bilan Simplifié")
    asset_value = st.number_input("Valeur Actifs (MV)", value=1000.0, step=100.0)
    asset_duration = st.slider("Duration Actif", 0.0, 20.0, 5.0, help="Sensibilité moyenne des actifs aux taux")
    
    liab_value = st.number_input("Best Estimate Passif (BEL)", value=900.0, step=100.0)
    liab_duration = st.slider("Duration Passif", 0.0, 30.0, 15.0, help="Sensibilité moyenne du passif aux taux")

# --- 2. CALCULS DES COURBES ---
t = np.linspace(0.1, 40, 100)
term1 = (1 - np.exp(-t/tau)) / (t/tau)
term2 = term1 - np.exp(-t/tau)
r_base = b0 + b1*term1 + b2*term2

# Fonction d'approximation des chocs S2 (Simplification pédagogique des vecteurs officiels)
def get_s2_shocks(t_arr):
    # Points de référence (Maturité, Choc Up, Choc Down)
    # Source approx : Delegated Regulation
    mats = [0.25, 1, 5, 10, 20, 90]
    ups =  [0.70, 0.70, 0.40, 0.42, 0.26, 0.20] # +70% court terme, +26% long terme
    downs = [-0.75, -0.75, -0.40, -0.31, -0.28, -0.20] # -75% court terme
    
    s_up = np.interp(t_arr, mats, ups)
    s_down = np.interp(t_arr, mats, downs)
    return s_up, s_down

s_up, s_down = get_s2_shocks(t)

# Application des chocs (Modèle multiplicatif simple pour taux positifs)
r_up = r_base * (1 + s_up)
r_down = r_base * (1 + s_down)

# --- 3. VISUALISATION ---
st.subheader("Visualisation des Scénarios de Choc")
fig = go.Figure()
fig.add_trace(go.Scatter(x=t, y=r_base*100, name="Courbe Centrale", line=dict(color='black', width=3)))
fig.add_trace(go.Scatter(x=t, y=r_up*100, name="Choc UP (Hausse)", line=dict(color='red', dash='dot')))
fig.add_trace(go.Scatter(x=t, y=r_down*100, name="Choc DOWN (Baisse)", line=dict(color='green', dash='dot')))
fig.update_layout(title="Déformation de la courbe des taux (Chocs relatifs)", xaxis_title="Maturité (Années)", yaxis_title="Taux (%)", hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)

# --- 4. CALCUL D'IMPACT (APPROCHE DURATION) ---
# Pour estimer l'impact sans revaloriser ligne à ligne, on utilise l'approximation : Delta V = - Duration * Delta r * V
# On cherche le choc de taux moyen à la maturité correspondant à la duration
idx_asset = np.searchsorted(t, asset_duration)
idx_liab = np.searchsorted(t, liab_duration)

# Choc absolu de taux à ces points (ex: +1.5%)
dr_up_asset = r_up[min(idx_asset, 99)] - r_base[min(idx_asset, 99)]
dr_down_asset = r_down[min(idx_asset, 99)] - r_base[min(idx_asset, 99)]

dr_up_liab = r_up[min(idx_liab, 99)] - r_base[min(idx_liab, 99)]
dr_down_liab = r_down[min(idx_liab, 99)] - r_base[min(idx_liab, 99)]

# Impact en Euros
delta_asset_up = - asset_duration * dr_up_asset * asset_value
delta_liab_up = - liab_duration * dr_up_liab * liab_value

delta_asset_down = - asset_duration * dr_down_asset * asset_value
delta_liab_down = - liab_duration * dr_down_liab * liab_value

# Impact NAV (Fonds Propres)
delta_nav_up = delta_asset_up - delta_liab_up
delta_nav_down = delta_asset_down - delta_liab_down

scr_taux = max(0, -delta_nav_up, -delta_nav_down)

# --- 5. RÉSULTATS ---
st.divider()
st.subheader("Résultats du SCR Taux")

col_res1, col_res2, col_res3 = st.columns(3)
col_res1.metric("Impact Scénario UP", f"{delta_nav_up:.1f} M€", delta_color="normal" if delta_nav_up > 0 else "inverse")
col_res2.metric("Impact Scénario DOWN", f"{delta_nav_down:.1f} M€", delta_color="normal" if delta_nav_down > 0 else "inverse")
col_res3.metric("SCR Taux Retenu", f"{scr_taux:.1f} M€", delta="-SCR", delta_color="inverse")

# Graphique Waterfall
fig_waterfall = go.Figure(data=[
    go.Bar(name='Impact Actif', x=['Scénario UP', 'Scénario DOWN'], y=[delta_asset_up, delta_asset_down], marker_color='blue'),
    go.Bar(name='Impact Passif (signe opposé)', x=['Scénario UP', 'Scénario DOWN'], y=[-delta_liab_up, -delta_liab_down], marker_color='orange'),
    go.Bar(name='Impact Net (NAV)', x=['Scénario UP', 'Scénario DOWN'], y=[delta_nav_up, delta_nav_down], marker_color=['red' if x<0 else 'green' for x in [delta_nav_up, delta_nav_down]])
])
fig_waterfall.update_layout(title="Décomposition Actif / Passif des impacts", barmode='group')
st.plotly_chart(fig_waterfall, use_container_width=True)

st.info(f"**Analyse :** Le scénario le plus défavorable est le scénario **{'DOWN' if delta_nav_down < delta_nav_up else 'UP'}**. Cela s'explique par le gap de duration : Duration Actif ({asset_duration} ans) vs Duration Passif ({liab_duration} ans).")
