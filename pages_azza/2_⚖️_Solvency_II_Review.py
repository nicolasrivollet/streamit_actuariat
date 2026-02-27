import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Réforme Solvabilité II | Analyse Globale", layout="wide")

# --- HEADER ---
st.title("⚖️ Révision de la Directive Solvabilité II")
st.markdown("""
La révision de la directive (souvent appelée 'Solvency II Review') constitue l'évolution la plus importante du cadre réglementaire depuis son entrée en vigueur en 2016. 
L'objectif est de recalibrer le système pour mieux refléter l'environnement de taux bas (à l'époque du lancement), encourager le financement de l'économie et intégrer les risques émergents.
""")

st.divider()

# --- SECTION 1 : PILIER 1 - CALCUL DU CAPITAL ---
st.header("1. Évolutions du Pilier 1 : Méthodologies de calcul")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Marge de Risque (RM)")
    st.write("""
    C'est l'un des changements les plus significatifs pour les assureurs Vie.
    * **Baisse du Coût du Capital (CoC) :** Passage de 6% à 4,75%.
    * **Facteur de réduction lambda ($\lambda$) :** Introduction d'un mécanisme de réduction dépendant de la durée des engagements (méthode exponentielle), permettant d'atténuer la sensibilité de la RM aux taux d'intérêt.
    * **Impact :** Réduction globale estimée de la RM entre 15% et 25%, libérant des fonds propres.
    """)

with col2:
    st.subheader("Ajustement pour Volatilité (VA)")
    st.write("""
    Le mécanisme est affiné pour être plus réactif aux spreads de crédit locaux.
    * **Composante nationale :** Renforcement de l'ajustement spécifique à chaque pays pour éviter les effets de pro-cyclicité.
    * **Seuil d'activation :** Simplification des critères de déclenchement pour mieux protéger le bilan en cas de crise systémique sur les marchés obligataires.
    """)

st.markdown("#### Taux d'intérêt et Extrapolation (Smith-Wilson)")
st.write("""
La révision modifie la méthode d'extrapolation de la courbe des taux. L'introduction d'une approche plus graduelle vers le **Taux Long Terme (UFR)** vise à mieux refléter les prix de marché au-delà du dernier point liquide (LLP), tout en évitant des sauts brutaux de valorisation des engagements.
""")

st.divider()

# --- SECTION 2 : ESG ET RISQUES DURABLES ---
st.header("2. Intégration des risques de durabilité")

st.markdown("""
La réforme grave dans le marbre réglementaire la prise en compte du changement climatique.
* **Analyses de scénarios :** Obligation pour les assureurs d'inclure des scénarios de changement climatique à long terme (5 à 10 ans et +30 ans) dans leur évaluation interne (ORSA).
* **Double matérialité :** Évaluation de l'impact de l'entreprise sur l'environnement et de l'environnement sur l'entreprise.
* **Pillar 1 'Green' :** Mandat donné à l'EIOPA pour explorer des traitements prudentiels différenciés pour les actifs exposés aux risques environnementaux ou sociaux.
""")

st.divider()

# --- SECTION 3 : MACRO-PRUDENCE ET SURVEILLANCE ---
st.header("3. Nouveau cadre Macro-Prudentiel")

st.write("""
Au-delà de la solvabilité individuelle, les autorités de contrôle (ACPR, EIOPA) reçoivent de nouveaux mandats pour surveiller le risque systémique.
""")

tab1, tab2, tab3 = st.tabs(["Liquidité", "Proportionnalité", "Reporting"])

with tab1:
    st.markdown("**Gestion de la liquidité :** Les superviseurs pourront exiger des plans de gestion de la liquidité plus stricts et, dans des cas extrêmes, suspendre temporairement les droits de rachat des assurés.")

with tab2:
    st.markdown("**Principe de proportionnalité :** Création d'une catégorie d'entreprises à 'faible profil de risque' bénéficiant d'allègements automatiques sur le reporting et la gouvernance, réduisant les coûts de conformité.")

with tab3:
    st.markdown("**Reporting (Pilier 3) :** Révision des QRT (Quantitative Reporting Templates) pour rationaliser les informations demandées et améliorer la comparabilité des rapports publics (SFCR).")

st.divider()



st.caption("Document de synthèse basé sur les textes de la Commission Européenne et du Parlement - 2026")