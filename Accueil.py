import streamlit as st

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Portfolio Actuariat & Risques",
    page_icon="📊",
    layout="wide"
)

# --- 2. DÉFINITION DES PAGES ---

# La page d'accueil pointe vers une fonction interne ou le fichier lui-même
# Pour éviter la répétition, nous allons définir une fonction pour le contenu de l'accueil
def show_home():
    st.title("Système de Pilotage des Risques & Actuariat")
    st.caption("🚀 Portfolio Technique - Nicolas Rivollet")
    
    st.markdown("""
    ### Bienvenue sur mon Portfolio d'Expertise
    
    Ce site regroupe mes travaux de modélisation et mes analyses stratégiques dans le secteur de l'assurance et de la finance. 
    Il a été conçu pour démontrer l'application de **Python** aux problématiques actuarielles modernes.
    
    #### 🎯 Objectifs du projet
    1.  **Finance & ALM** : Modélisation interactive des taux (Nelson-Siegel, Smith-Wilson).
    2.  **Réglementation** : Outils de calcul et de visualisation pour Solvabilité II (SCR, Best Estimate).
    3.  **Data Science** : Automatisation des processus actuariels via des dashboards web.
    
    ---
    #### 🛠 Stack Technique
    *   **Langage :** Python 3.10+
    *   **Interface :** Streamlit
    *   **Calculs :** NumPy, Pandas, Scipy
    *   **Visualisation :** Plotly Interactive
    """)
    
    st.info("👈 **Utilisez le menu latéral pour naviguer à travers les différents modules de modélisation.**")

    # Ajout d'une section contact dans la sidebar pour le recrutement
    with st.sidebar:
        st.header("📬 Contact & Profil")
        st.markdown("Si ce profil vous intéresse pour une opportunité :")
        st.link_button("Mon Profil LinkedIn", "https://www.linkedin.com/in/nicolasrivollet/") # Remplacez par votre vrai lien si besoin
        st.link_button("Code Source (GitHub)", "https://github.com/nicolasrivollet")

        st.markdown("---")
        # Bouton de téléchargement du CV
        import os
        cv_file = "cv_RivolletNicolas_v2602-5.pdf"
        if os.path.exists(cv_file):
            with open(cv_file, "rb") as pdf:
                st.download_button(label="📄 Télécharger mon CV", data=pdf, file_name="cv_RivolletNicolas_v2602-5.pdf", mime="application/pdf")

# Définition des objets pages
# Note : Pour l'accueil, on passe la fonction show_home au lieu du nom du fichier
home_page = st.Page(show_home, title="Présentation", icon="🏠", default=True)

nelsonSiegel = st.Page(
    "modules/courbe_taux.py", 
    title="Modèle Nelson-Siegel", 
    icon="📉"
)

comparatif_modeles = st.Page(
    "modules/comparatif_modeles.py", 
    title="Modélisation Courbe de Taux (intro)", 
    icon="🔬"
)

scr_screener = st.Page(
    "modules/scr_screener.py", 
    title="SCR Asset Screener",
    icon="🔬"
)

smith_wilson = st.Page(
    "modules/smith_wilson.py", 
    title="Modèle Smith-Wilson", 
    icon="📏"
)


s2_review = st.Page(
    "modules/reforme_s2.py", 
    title="Réforme Solvabilité II", 
    icon="⚖️"
)

volatility_adjustment = st.Page(
    "modules/volatility_adjustment.py",
    title="Volatility Adjustment",
    icon="🛡️"
)

chain_ladder = st.Page(
    "modules/provisionnement_IARD.py",
    title="Chain-Ladder",
    icon="📊"
)

scr_taux = st.Page(
    "modules/scr_taux.py",
    title="SCR Taux (Standard)",
    icon="📉"
)

pilotage_reass = st.Page(
    "modules/politage_reassu.py",
    title="Pilotage Réassurance",
    icon="📉"
)

lee_carter = st.Page(
    "modules/mortalite_lee_carter.py",
    title="Mortalité (Lee-Carter)",
    icon="💀"
)

# --- 3. NAVIGATION ---

pg = st.navigation({
    "Général": [home_page],
    "Assurance Vie": [lee_carter],
    "Provisionnement": [chain_ladder],
    "Finance & ALM": [comparatif_modeles, nelsonSiegel, smith_wilson, pilotage_reass], 
    "Réglementation & ESG": [s2_review, scr_screener, volatility_adjustment, scr_taux],
})

# --- 4. EXÉCUTION ---
# pg.run() s'occupe de tout : 
# - Si home_page est sélectionnée, il exécute show_home()
# - Si une autre page est sélectionnée, il exécute le fichier .py correspondant
pg.run()