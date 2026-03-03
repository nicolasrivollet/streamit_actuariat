import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Simulateur ALM Fonds Euros", layout="wide")

st.title("🏦 Simulateur ALM : Projection Fonds Euros")
st.subheader("Pilotage de la Participation aux Bénéfices et de la Solvabilité")

st.markdown("""
Ce module simule la projection bilantielle d'un fonds en euros sur 20 ans.
L'objectif est de piloter le **Taux Servi** aux assurés en jouant sur la **PPB (Provision pour Participation aux Bénéfices)** pour lisser les rendements et assurer la solvabilité.
""")

st.divider()

# --- 1. HYPOTHÈSES ---
st.header("1. Hypothèses de Projection")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Bilan Initial")
    aum_initial = st.number_input("Actif Géré (M€)", 100.0, 10000.0, 1000.0, step=100.0)
    pm_initial = aum_initial * 0.92 # 8% de fonds propres initiaux
    ppb_initial = st.number_input("Stock PPB Initial (M€)", 0.0, 100.0, 20.0, step=5.0, help="Réserve de bénéfices non distribués.")
    
with col2:
    st.subheader("Actif (Rendement)")
    alloc_bond = st.slider("Allocation Obligations (%)", 0, 100, 80, 5) / 100
    yield_bond = st.slider("Rendement Obligataire (%)", 0.0, 6.0, 2.5, 0.1) / 100
    yield_equity = st.slider("Rendement Actions (%)", -10.0, 20.0, 6.0, 0.5) / 100

with col3:
    st.subheader("Passif (Coût)")
    tmg = st.slider("Taux Minimum Garanti (TMG) %", 0.0, 3.0, 0.5, 0.1) / 100
    target_rate = st.slider("Taux Cible Concurrents (%)", 0.0, 6.0, 3.0, 0.1) / 100
    frais_gestion = 0.006 # 0.60%

# --- 2. MOTEUR DE PROJECTION ---
horizon = 20
years = np.arange(1, horizon + 1)

# Stockage des résultats
res_yield_asset = []
res_rate_served = []
res_ppb_stock = []
res_solvency = []

# Variables d'état
curr_aum = aum_initial
curr_pm = pm_initial
curr_ppb = ppb_initial

for t in range(horizon):
    # 1. Rendement Financier
    # Hypothèse simplifiée : Rendement comptable = Rendement financier (pas de lissage des plus-values latentes ici)
    fin_result = curr_aum * (alloc_bond * yield_bond + (1 - alloc_bond) * yield_equity)
    
    # 2. Chargements Passif
    tech_cost = curr_pm * tmg
    fees = curr_pm * frais_gestion
    
    # 3. Marge Financière Brute
    gross_margin = fin_result - tech_cost - fees
    
    # 4. Politique de PB (Participation aux Bénéfices)
    # On doit servir au moins le TMG.
    # On vise le Taux Cible pour rester compétitif.
    # Le besoin de PB additionnelle = (Taux Cible - TMG) * PM
    
    pb_target = max(0, (target_rate - tmg) * curr_pm)
    
    # Solde de l'exercice (Marge disponible pour financer la cible)
    solde = gross_margin - pb_target
    
    if solde >= 0:
        # Cas favorable : On a assez de marge pour servir la cible
        pb_distributed = pb_target
        dotation_ppb = solde
        reprise_ppb = 0
        
        # Plafond de PPB (ex: 8% des PM) : si on a trop de réserves, on distribue le surplus
        max_ppb = 0.08 * curr_pm
        if (curr_ppb + dotation_ppb) > max_ppb:
             surplus = (curr_ppb + dotation_ppb) - max_ppb
             pb_distributed += surplus
             dotation_ppb -= surplus
    else:
        # Cas défavorable : On manque de marge pour atteindre la cible
        besoin = -solde
        # On reprend de la PPB pour combler le trou (limité au stock disponible)
        reprise_ppb = min(curr_ppb, besoin)
        dotation_ppb = 0
        # Ce qu'on distribue = Marge de l'année + Reprise
        pb_distributed = max(0, gross_margin + reprise_ppb)

    # Taux servi final
    rate_served = tmg + (pb_distributed / curr_pm) if curr_pm > 0 else 0
    
    # Mise à jour des stocks
    curr_ppb = curr_ppb + dotation_ppb - reprise_ppb
    
    # Evolution PM (Capitalisation des intérêts versés aux assurés)
    # Le taux servi est net de frais, donc la PM grossit de ce taux.
    curr_pm = curr_pm * (1 + rate_served)
    
    # Evolution Aum (Simplifié : suit le rendement financier)
    # Hypothèse : Pas de rachats ni de nouvelles primes pour isoler l'effet rendement
    # Les frais de gestion sont prélevés sur l'actif (cash out pour l'assureur)
    curr_aum = curr_aum + fin_result - fees
    
    # Stockage
    res_yield_asset.append((fin_result / curr_aum) if curr_aum > 0 else 0)
    res_rate_served.append(rate_served)
    res_ppb_stock.append(curr_ppb)
    
    # Proxy Solvabilité S2 (Vision Économique)
    # 1. Fonds Propres Économiques = FP Comptables + VIF (Value In Force)
    # VIF proxy : Valeur actuelle des marges futures (~1.5% des PM)
    vif = curr_pm * 0.015
    own_funds_s2 = (curr_aum - curr_pm - curr_ppb) + vif
    
    # 2. SCR (Capital Requis) avec LAC TP
    # Choc Brut = Choc Marché (Actions) + Choc Vie/Op (Proxy 3% PM)
    scr_brut = (curr_aum * (1-alloc_bond) * 0.39) + (curr_pm * 0.03)
    # LAC TP : On suppose que 50% du choc est absorbé par la baisse de la PB future
    scr_net = scr_brut * (1 - 0.50)
    
    res_solvency.append(own_funds_s2 / scr_net if scr_net > 0 else 0)

# --- 3. VISUALISATION ---
st.header("2. Résultats de la Projection")

col_res1, col_res2 = st.columns(2)

with col_res1:
    # Graphique Taux
    fig_rates = go.Figure()
    fig_rates.add_trace(go.Scatter(x=years, y=np.array(res_yield_asset)*100, name="Rendement Actif", line=dict(color='blue')))
    fig_rates.add_trace(go.Scatter(x=years, y=np.array(res_rate_served)*100, name="Taux Servi (Net)", line=dict(color='green', width=3)))
    fig_rates.add_hline(y=target_rate*100, line_dash="dash", line_color="gray", annotation_text="Cible Concurrents")
    fig_rates.add_hline(y=tmg*100, line_dash="dot", line_color="red", annotation_text="TMG")

    fig_rates.update_layout(title="Pilotage du Taux Servi vs Rendement Actif", xaxis_title="Année", yaxis_title="Taux (%)")
    st.plotly_chart(fig_rates, use_container_width=True)

with col_res2:
    # Graphique PPB
    fig_ppb = go.Figure()
    fig_ppb.add_trace(go.Bar(x=years, y=res_ppb_stock, name="Stock PPB", marker_color='orange'))
    fig_ppb.update_layout(title="Évolution de la Provision pour Participation aux Bénéfices (PPB)", xaxis_title="Année", yaxis_title="Montant (M€)")
    st.plotly_chart(fig_ppb, use_container_width=True)

st.info("""
**Mécanique ALM :**
*   Si le **Rendement Actif > Taux Cible**, l'assureur sert le taux cible et met le surplus en **PPB**.
*   Si le **Rendement Actif < Taux Cible**, l'assureur reprend de la **PPB** pour soutenir le taux servi.
*   Si la PPB est épuisée, le taux servi tombe au niveau du rendement actif (voire au TMG si krach).
""")