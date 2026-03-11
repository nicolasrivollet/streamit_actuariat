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

st.header("1. Saisie des Caractéristiques du Support")

# --- CORPS DE LA PAGE ---
col_input1, col_input2, col_input3 = st.columns(3)

# --- CONFIGURATION DYNAMIQUE DES SEUILS (NOUVEAU) ---
with st.expander("⚙️ Configurer les Seuils de la Politique Risque (Hard Limits)", expanded=True):
    col_conf1, col_conf2, col_conf3, col_conf4 = st.columns(4)
    limit_aum = col_conf1.number_input("Min AUM (M€)", 0, 1000, 50, help="Seuil de liquidité")
    limit_track = col_conf2.number_input("Min Historique (Ans)", 0, 10, 3)
    limit_sri = col_conf3.slider("Max SRI (Risque)", 1, 7, 5)
    limit_fees = col_conf4.number_input("Max Frais (%)", 0.0, 5.0, 2.5, 0.1)
    exclude_art6 = st.checkbox("Exclure systématiquement Article 6 (ESG)", value=True)
with col_input1:
    st.subheader("📝 Identité")
    fund_name = st.text_input("Nom du Fonds", "Carmignac Patrimoine A")
    isin = st.text_input("Code ISIN", "FR0010135103")
    category = st.selectbox("Classe d'Actifs", 
                            ["Actions Monde", "Actions Europe", "Obligations Euro", "Diversifié", "Immobilier (SCI/OPCI/SCPI)", "Produit Structuré"])

with col_input2:
    st.subheader("📊 Quantitatif")
    aum = st.number_input("Encours du fonds (M€)", 0, 50000, 450)
    track_record = st.number_input("Historique (Années)", 0, 50, 8)
    volatility = st.number_input("Volatilité 3 ans (%)", 0.0, 100.0, 12.5, 0.1)

with col_input3:
    st.subheader("🌿 ESG & Frais")
    sri = st.slider("SRI (Indicateur Risque 1-7)", 1, 7, 3)
    sfdr = st.selectbox("Classification SFDR", ["Article 6 (Standard)", "Article 8 (Light Green)", "Article 9 (Dark Green)"], index=1)
    fees_mgt = st.number_input("Frais de Gestion Max (%)", 0.0, 5.0, 1.80, 0.05)
    retrocession = st.number_input("Rétrocessions (%)", 0.0, 2.0, 0.85, 0.05)

st.divider()

col1, col2 = st.columns([1.5, 1])

with col1:
    st.header("2. Analyse d'Éligibilité (Hard Limits)")
    st.caption("Conformité par rapport à la **Politique de Souscription** (paramétrable ci-dessus).")

    # Définition des règles
    rules = {
        "Liquidité & Profondeur": {"Seuil": f"AUM > {limit_aum} M€", "Check": aum >= limit_aum, "Explication": "Éviter le risque de liquidité en cas de rachat massif."},
        "Stabilité de Gestion": {"Seuil": f"Historique > {limit_track} ans", "Check": track_record >= limit_track, "Explication": "Nécessité d'évaluer la performance sur un cycle complet."},
        "Plafond de Risque (Retail)": {"Seuil": f"SRI <= {limit_sri}", "Check": sri <= limit_sri, "Explication": "Limitation du risque de marché pour la clientèle standard."},
        "Ambition ESG": {"Seuil": "Pas d'Article 6" if exclude_art6 else "Aucun", "Check": ("Article 6" not in sfdr) if exclude_art6 else True, "Explication": "Alignement avec la trajectoire Net Zero du Groupe."},
        "Compétitivité Prix": {"Seuil": f"Frais Gestion < {limit_fees}%", "Check": fees_mgt < limit_fees, "Explication": "Protection de la performance nette pour l'assuré."}
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
    
    # Benchmark (Moyenne catégorie fictive)
    scores_bench = [60, 50, 60, 70] # Valeurs moyennes fixes pour l'exemple

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=scores, theta=categories, fill='toself', name=fund_name))
    fig_radar.add_trace(go.Scatterpolar(r=scores_bench, theta=categories, name='Moyenne Marché', line=dict(dash='dot', color='gray')))
    
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True, 
                            legend=dict(orientation="h", y=-0.2), title="Profil du Support vs Marché", height=350, margin=dict(t=30, b=20))
    st.plotly_chart(fig_radar, use_container_width=True)

st.info("💡 **Note pour l'entretien :** Ce module est désormais paramétrable. Il démontre ma capacité à créer des outils flexibles où le Risk Management peut ajuster ses seuils d'appétence (Hard Limits) sans toucher au code.")