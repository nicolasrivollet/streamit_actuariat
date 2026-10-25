import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="ESG & Investissements", layout="wide")

st.title("Intégration ESG dans la Gestion d'Actifs")
st.subheader("Stratégies d'Investissement Durable & Réglementation SFDR")

st.markdown("""
L'intégration des critères **Environnementaux, Sociaux et de Gouvernance (ESG)** n'est plus une option de niche mais une exigence réglementaire et stratégique.
Les assureurs, en tant qu'investisseurs institutionnels majeurs, doivent aligner leur politique d'investissement sur des objectifs de durabilité (Directive Solvabilité II - Principe de la Personne Prudente amendé).
""")

st.divider()

# --- 1. LES STRATÉGIES ESG ---
st.header("1. Les Stratégies d'Investissement Responsable")
st.markdown("Il n'y a pas une seule façon de faire de l'ESG. Voici les principales approches :")

col1, col2 = st.columns(2)

with col1:
    st.info("### Exclusion (Negative Screening)")
    st.write("Exclure les secteurs controversés (Tabac, Armement, Charbon) ou les entreprises ne respectant pas les normes internationales (UN Global Compact).")
    
    st.success("### Best-in-Class")
    st.write("Sélectionner les émetteurs les mieux notés sur les critères ESG au sein de leur secteur d'activité, sans exclure de secteur a priori.")

with col2:
    st.warning("### Thématique")
    st.write("Investir dans des secteurs liés au développement durable (Énergies renouvelables, Eau, Gestion des déchets).")
    
    st.error("### Impact Investing")
    st.write("Investissements réalisés avec l'intention de générer un impact social ou environnemental positif et mesurable, en plus d'un rendement financier.")

st.divider()

# --- 2. SIMULATEUR D'IMPACT ---
st.header("2. Simulation d'Impact sur le Portefeuille")
st.markdown("Ajustez l'allocation pour voir l'impact sur le Score ESG et l'Empreinte Carbone.")

# Hypothèses simplifiées
# Actif Classique : Score ESG 50/100, Carbone 200 tCO2/M€
# Actif ESG (Best-in-Class) : Score ESG 75/100, Carbone 120 tCO2/M€
# Actif Vert (Impact) : Score ESG 90/100, Carbone 50 tCO2/M€

col_sim1, col_sim2 = st.columns([1, 2])

with col_sim1:
    st.subheader("Allocation Cible")
    # Approche en cascade pour garantir 100%
    part_esg = st.slider("1. Part Investissement Responsable (%)", 0, 100, 50, step=5, help="Part du portefeuille soumise à des critères ESG.")
    
    part_impact = 0
    if part_esg > 0:
        part_impact = st.slider("2. Dont part 'Impact / Vert' (%)", 0, 100, 40, step=5, help="Au sein de la poche ESG, part dédiée à l'impact fort (Article 9).")
    
    # Calcul des poids (somme = 100%)
    w_classic = (100 - part_esg) / 100.0
    w_impact = (part_esg / 100.0) * (part_impact / 100.0)
    w_bic = (part_esg / 100.0) * (1 - part_impact / 100.0)
    
    st.caption(f"**Répartition :**\n- Classique : {w_classic:.0%}\n- Best-in-Class : {w_bic:.0%}\n- Impact : {w_impact:.0%}")

with col_sim2:
    # Calculs
    score_esg = w_classic * 50 + w_bic * 75 + w_impact * 90
    carbon = w_classic * 200 + w_bic * 120 + w_impact * 50
    
    # Benchmark (Indice de marché standard)
    bench_esg = 55
    bench_carbon = 180
    
    st.subheader("Résultats Extra-Financiers")
    
    c1, c2 = st.columns(2)
    c1.metric("Score ESG Portefeuille", f"{score_esg:.1f}/100", delta=f"{score_esg - bench_esg:.1f} vs Benchmark")
    c2.metric("Intensité Carbone", f"{carbon:.0f} tCO2/M€", delta=f"{carbon - bench_carbon:.0f} vs Benchmark", delta_color="inverse")
    
    # Graphique Radar
    categories = ['Environnement', 'Social', 'Gouvernance', 'Carbone (Inversé)', 'Controverses (Inversé)']
    
    # Simulation de sous-scores
    r_port = [
        score_esg * 1.1 if w_impact > 0.3 else score_esg, 
        score_esg * 0.9, 
        score_esg, 
        (300 - carbon)/3, # Scaling pour le radar
        score_esg * 1.05
    ]
    r_bench = [55, 55, 55, (300-180)/3, 50]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=r_port, theta=categories, fill='toself', name='Portefeuille Simulé'))
    fig.add_trace(go.Scatterpolar(r=r_bench, theta=categories, fill='toself', name='Benchmark Marché'))
    
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True, title="Profil Extra-Financier")
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# --- 3. CADRE RÉGLEMENTAIRE SFDR ---
st.header("3. Classification SFDR (Sustainable Finance Disclosure Regulation)")
st.markdown("Le règlement SFDR impose aux acteurs financiers de classer leurs produits selon leur niveau d'ambition durable.")

col_sfdr1, col_sfdr2, col_sfdr3 = st.columns(3)

with col_sfdr1:
    st.markdown("### 📄 Article 6\n**Produits Classiques**")
    st.write("Produits qui intègrent les risques ESG dans le processus d'investissement, mais sans objectif de durabilité affiché.")

with col_sfdr2:
    st.markdown("### 🌱 Article 8\n**Produits 'Light Green'**")
    st.write("Produits qui promeuvent des caractéristiques environnementales ou sociales (ex: exclusion, best-in-class).")

with col_sfdr3:
    st.markdown("### 🌳 Article 9\n**Produits 'Dark Green'**")
    st.write("Produits ayant un **objectif d'investissement durable** concret (ex: fonds climat aligné Accord de Paris).")

st.info("**Taxonomie Européenne :** En plus de SFDR, les assureurs doivent reporter la part de leurs investissements éligibles et alignés avec la Taxonomie verte (activités durables).")