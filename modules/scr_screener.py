import streamlit as st
import pandas as pd
import numpy as np

def calculate_scr_market(asset_type, value, rating=None, duration=0):
    """
    Calcule une estimation simplifiée du SCR Marché (Formule Standard S2)
    """
    scr_components = {}
    
    # 1. Choc Action (Type 1: Cotées, Type 2: Non-cotées/PE)
    if asset_type == "Actions":
        scr_components['Equity'] = value * 0.39 # Simplification Type 1
    
    # 2. Choc Spread (Basé sur le rating et la duration)
    elif asset_type == "Obligations":
        # Table simplifiée des facteurs de stress Spread
        stress_factors = {"AAA": 0.009, "AA": 0.011, "A": 0.014, "BBB": 0.025}
        factor = stress_factors.get(rating, 0.045) # High yield par défaut
        scr_components['Spread'] = value * duration * factor
        
    # 3. Choc Immobilier
    elif asset_type == "Immobilier":
        scr_components['Property'] = value * 0.25
        
    return scr_components

# --- INTERFACE STREAMLIT ---
st.title("🛡️ SCR Asset Screener")
st.subheader("Analyse d'impact Capital & Rentabilité (GACM)")

with st.sidebar:
    st.header("Nouvel Investissement")
    name = st.text_input("Nom de l'actif", "Obligation Corporate A")
    asset_type = st.selectbox("Classe d'actif", ["Obligations", "Actions", "Immobilier"])
    nominal = st.number_input("Montant investi (€)", value=1_000_000)
    yield_expected = st.slider("Rendement attendu (%)", 0.0, 10.0, 4.5) / 100
    
    if asset_type == "Obligations":
        rating = st.select_slider("Rating", options=["AAA", "AA", "A", "BBB", "HY"])
        duration = st.number_input("Sensibilité (Duration)", value=5.5)
    else:
        rating, duration = None, 0

# --- CALCULS ---
res = calculate_scr_market(asset_type, nominal, rating, duration)
scr_total = sum(res.values()) # Simplification : Somme brute (hors corrélations)
roi_net_capital = (nominal * yield_expected) / scr_total if scr_total > 0 else 0

# --- AFFICHAGE ---
col1, col2, col3 = st.columns(3)
col1.metric("Capital Immobilisé (SCR)", f"{scr_total:,.0f} €")
col2.metric("Consommation de Fonds Propres", f"{(scr_total/nominal):.1%}")
col3.metric("RAROC", f"{roi_net_capital:.2%}")

st.info(f"**Analyse :** Pour investir dans cet actif, le GACM doit bloquer **{scr_total:,.0f} €** de fonds propres.")