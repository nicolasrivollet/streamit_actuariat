import streamlit as st

# --- CONFIGURATION GLOBALE ---
st.set_page_config(
    page_title="Portfolio Actuariat & Risques",
    page_icon="📊",
    layout="wide"
)

# --- DÉFINITION DES PAGES ---
# On définit chaque page avec son chemin de fichier, son titre et son icône

# Section Général
home_page = st.Page(
    "Accueil.py", 
    title="Présentation", 
    icon="🏠", 
    default=True
)

# Section Finance & ALM
yield_curve = st.Page(
    "modules/courbe_taux.py", 
    title="Modélisation Courbe de Taux", 
    icon="📉"
)

# Section Réglementation & ESG
s2_review = st.Page(
    "modules/reforme_s2.py", 
    title="Réforme Solvabilité II", 
    icon="⚖️"
)

# Section Expertise Technique (Placeholder pour le moment)
# chain_ladder = st.Page("modules/chain_ladder.py", title="Provisionnement Non-Vie", icon="🛡️")

# --- NAVIGATION THÉMATIQUE ---
# C'est ici que l'on crée les sections visuelles dans la barre latérale
pg = st.navigation({
    "Général": [home_page],
    "Finance & ALM": [yield_curve],
    "Réglementation & ESG": [s2_review],
    # "Expertise Technique": [chain_ladder],
})

# --- AFFICHAGE DU CONTENU DE L'ACCUEIL ---
# Cette partie ne s'affiche QUE si on est sur la page home_page
if st.get_option("client.showSidebarNavigation"): # Vérification interne Streamlit
    
    # On n'affiche le contenu de l'accueil que si la page active est l'accueil
    # Sinon, pg.run() s'occupe d'afficher le contenu des autres fichiers
    pass

def show_home():
    st.title("Système de Pilotage des Risques & Actuariat")
    st.markdown(f"""
    ### Bienvenue sur mon Portfolio d'Expertise
    
    Ce site regroupe mes travaux de modélisation et mes analyses stratégiques dans le secteur de l'assurance et de la finance. 
    Il est structuré autour de **4 thématiques clés** pour répondre aux enjeux actuels des directions des risques :
    
    1.  **Finance & ALM** : Modélisation des taux et adossement actif-passif.
    2.  **Réglementation & ESG** : Veille et impact des réformes (Solvabilité II, IFRS 17).
    3.  **Expertise Technique** : Provisionnement et tarification.
    4.  **Data Science** : Automatisation et analyses prédictives.
    
    ---
    **Utilisez le menu à gauche pour naviguer entre les modules.**
    """)
    
    st.info("💡 **Note technique :** Cette plateforme est développée en Python avec Streamlit pour garantir une interactivité totale avec les modèles mathématiques.")

# Logique d'exécution
if st.experimental_user.get("email"): # Juste pour s'assurer que l'app tourne
    pass

# Lancement du moteur de navigation
# Si la page actuelle est l'accueil, on affiche le contenu show_home()
# Sinon, pg.run() va chercher le code dans le dossier /modules/
if pg.title == "Présentation":
    show_home()
    pg.run()
else:
    pg.run()