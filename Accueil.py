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
    st.markdown("""
    ### Bienvenue sur mon Portfolio d'Expertise
    
    Ce site regroupe mes travaux de modélisation et mes analyses stratégiques dans le secteur de l'assurance et de la finance. 
    Il est structuré autour de **4 thématiques clés** :
    
    1.  **Finance & ALM** : Modélisation des taux et adossement actif-passif.
    2.  **Réglementation & ESG** : Veille et impact des réformes (Solvabilité II, IFRS 17).
    3.  **Expertise Technique** : Provisionnement et tarification.
    4.  **Data Science** : Automatisation et analyses prédictives.
    
    ---
    **Utilisez le menu à gauche pour naviguer entre les modules.**
    """)
    st.info("💡 **Note technique :** Cette plateforme est développée en Python avec Streamlit pour garantir une interactivité totale.")

# Définition des objets pages
# Note : Pour l'accueil, on passe la fonction show_home au lieu du nom du fichier
home_page = st.Page(show_home, title="Présentation", icon="🏠", default=True)

yield_curve = st.Page(
    "modules/courbe_taux.py", 
    title="Modélisation Courbe de Taux", 
    icon="📉"
)

comparatif_modeles = st.Page(
    "modules/comparatif_modeles.py", 
    title="Comparatif des Méthodes", 
    icon="🔬"
)

s2_review = st.Page(
    "modules/reforme_s2.py", 
    title="Réforme Solvabilité II", 
    icon="⚖️"
)

# --- 3. NAVIGATION ---

pg = st.navigation({
    "Général": [home_page],
    "Finance & ALM": [yield_curve, comparatif_modeles], # Ajouté ici
    "Réglementation & ESG": [s2_review],
})

# --- 4. EXÉCUTION ---
# pg.run() s'occupe de tout : 
# - Si home_page est sélectionnée, il exécute show_home()
# - Si une autre page est sélectionnée, il exécute le fichier .py correspondant
pg.run()