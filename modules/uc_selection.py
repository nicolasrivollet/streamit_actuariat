import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Sélection & Due Diligence UC", layout="wide")

st.title("✅ Critères de Sélection & Référencement UC")
st.subheader("Operationalisation de la Politique de Souscription")

st.markdown("""
Cet outil permet d'évaluer l'éligibilité d'un nouveau support en Unités de Compte (UC) par rapport aux normes de risques définies par le Groupe.
Il combine des **critères d'exclusion (Hard Limits)** et un **scoring multicritère (Soft Limits)** pour émettre un avis risque.
""")

st.divider()

# --- SIDEBAR : FICHE D'IDENTITÉ DU FONDS ---
st.sidebar.header("📝 Fiche Fonds")

fund_name = st.sidebar.text_input("Nom du Fonds", "Carmignac Patrimoine A")
isin = st.sidebar.text_input("Code ISIN", "FR0010135103")
category = st.sidebar.selectbox("Classe d'Actifs", 
                                ["Actions Monde", "Actions Europe", "Obligations Euro", "Diversifié", "Immobilier (SCI/OPCI/SCPI)", "Produit Structuré"])

st.sidebar.subheader("Données Quantitatives")
aum = st.sidebar.number_input("Encours du fonds (M€)", 0, 50000, 450)
track_record = st.sidebar.slider("Historique (Années)", 0, 30, 8)
volatility = st.sidebar.slider("Volatilité 3 ans (%)", 0.0, 40.0, 12.5)
sri = st.sidebar.slider("SRI (Indicateur Risque 1-7)", 1, 7, 3)

st.sidebar.subheader("Données Qualitatives & ESG")
sfdr = st.sidebar.selectbox("Classification SFDR", ["Article 6 (Standard)", "Article 8 (Light Green)", "Article 9 (Dark Green)"], index=1)
fees_mgt = st.sidebar.number_input("Frais de Gestion Max (%)", 0.0, 5.0, 1.80, 0.05)
retrocession = st.sidebar.number_input("Rétrocessions (%)", 0.0, 2.0, 0.85, 0.05)


# --- CORPS DE LA PAGE ---

col1, col2 = st.columns([1.5, 1])

with col1:
    st.header("1. Filtres d'Éligibilité (Hard Limits)")
    st.info("Critères bloquants issus de la **Politique de Souscription et d'Investissement**.")

    # Définition des règles
    rules = {
        "Liquidité & Profondeur": {"Seuil": "AUM > 50 M€", "Check": aum >= 50, "Explication": "Éviter le risque de liquidité en cas de rachat massif."},
        "Stabilité de Gestion": {"Seuil": "Historique > 3 ans", "Check": track_record >= 3, "Explication": "Nécessité d'évaluer la performance sur un cycle complet."},
        "Plafond de Risque (Retail)": {"Seuil": "SRI <= 5", "Check": sri <= 5, "Explication": "Limitation du risque de marché pour la clientèle standard."},
        "Ambition ESG": {"Seuil": "Pas d'Article 6", "Check": "Article 6" not in sfdr, "Explication": "Alignement avec la trajectoire Net Zero du Groupe."},
        "Compétitivité Prix": {"Seuil": "Frais Gestion < 2.5%", "Check": fees_mgt < 2.5, "Explication": "Protection de la performance nette pour l'assuré."}
    }

    # Affichage des résultats
    compliance_status = True
    
    for rule_name, rule_data in rules.items():
        c1, c2, c3 = st.columns([2, 1.5, 3])
        
        c1.markdown(f"**{rule_name}**")
        
        if rule_data["Check"]:
            c2.success(f"✅ CONFORME")
        else:
            c2.error(f"❌ NON-CONFORME")
            compliance_status = False
            
        c3.caption(f"_{rule_data['Explication']}_")
        st.divider()

with col2:
    st.header("2. Scoring & Avis Risque")
    
    # Calcul d'un Score Synthétique (0-100)
    # Logique fictive pour l'exemple
    score_fin = min(100, (aum/1000 * 20) + (track_record/10 * 20)) # Robustesse
    score_esg = 100 if "Article 9" in sfdr else (70 if "Article 8" in sfdr else 20)
    score_perf = max(0, 100 - volatility * 2) # Performance ajustée du risque (proxy)
    score_frais = max(0, 100 - (fees_mgt * 30))
    
    global_score = 0.3 * score_fin + 0.3 * score_esg + 0.2 * score_perf + 0.2 * score_frais
    
    # Jauge de Score
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = global_score,
        title = {'text': "Score d'Attractivité"},
        gauge = {'axis': {'range': [0, 100]},
                 'bar': {'color': "#1565C0"},
                 'steps': [
                     {'range': [0, 50], 'color': "#FFEBEE"},
                     {'range': [50, 75], 'color': "#E3F2FD"},
                     {'range': [75, 100], 'color': "#E8F5E9"}]}
    ))
    fig_gauge.update_layout(height=250, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_gauge, use_container_width=True)

    st.subheader("Avis du Risk Manager")
    if compliance_status:
        if global_score > 70:
            st.success("### ✅ AVIS FAVORABLE\nLe support peut être référencé.")
        else:
            st.warning("### ⚠️ SOUS SURVEILLANCE\nConforme mais score faible (Watchlist).")
    else:
        st.error("### ⛔ REJETÉ (VETO)\nNon respect des critères bloquants.")

    # Radar Chart Détails
    categories = ['Robustesse Financière', 'ESG & Durabilité', 'Profil Rendement/Risque', 'Structure de Frais']
    scores = [score_fin, score_esg, score_perf, score_frais]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=scores, theta=categories, fill='toself', name=fund_name))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, 
                            title="Profil du Support", height=300, margin=dict(t=30, b=20))
    st.plotly_chart(fig_radar, use_container_width=True)

st.info("💡 **Note pour l'entretien :** Ce module illustre la déclinaison opérationnelle des normes d'actifs risques (Politique de Souscription) en un outil d'aide à la décision pour le référencement.")