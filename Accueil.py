import streamlit as st

import streamlit as st

# --- CONFIGURATION DES PAGES ---

# Page d'accueil
home_page = st.Page("Accueil.py", title="Introduction", icon="🏠", default=True)

# Thématique 1 : Finance & ALM
yield_curve = st.Page("modules/courbe_taux.py", title="Courbe de Taux (Nelson-Siegel)", icon="📉")

# Thématique 2 : Veille Réglementaire & ESG
s2_review = st.Page("modules/reforme_s2.py", title="Réforme Solvabilité II", icon="⚖️")

# Thématique 3 : Expertise Technique (À créer)
# chain_ladder = st.Page("modules/chain_ladder.py", title="Provisionnement Non-Vie", icon="🛡️")

# --- NAVIGATION THÉMATIQUE ---

pg = st.navigation({
    "Général": [home_page],
    "Finance & ALM": [yield_curve],
    "Réglementation & ESG": [s2_review],
    # Tu pourras ajouter les autres sections ici au fur et à mesure
    # "Expertise Technique": [chain_ladder],
})

# Lancement de l'application
pg.run()

st.set_page_config(page_title="Nicolas Rivollet | Portfolio Actuariat", layout="wide")

st.title("🚀 Nicolas Rivollet")
st.subheader("Expertise Actuarielle & Risk Management")

st.markdown("""
---
**Ingénieur CentraleSupélec | MS ESCP | Actuaire Certifié**
Ancien Head of Risk Management, je développe ici des outils de pilotage stratégique des risques.
""")

st.info("Utilisez le menu à gauche pour explorer les modules techniques.")