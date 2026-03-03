import streamlit as st
import os

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
    st.title("Bienvenue sur mon Portfolio")
    st.subheader("Nicolas RIVOLLET | Expert en Gestion des Risques et en Actuariat")
    
    col_video, col_text = st.columns(2)

    with col_video:
        # Vidéo de présentation depuis YouTube
        st.video("https://www.youtube.com/watch?v=your_video_id_here") # Remplacez par le lien de votre vidéo

    with col_text:
        st.markdown("""
        ### 👋 À propos de ce site
        
        Ce site est une vitrine interactive de mes compétences techniques et métiers. 
        Il regroupe des outils de modélisation, des analyses réglementaires et des tableaux de bord que j'ai développés pour illustrer mon savoir-faire en **Actuariat**, **Gestion des Risques** et **Data Science**.
        """)
    
    st.markdown("""
    ### 🤝 Prêt à échanger ?
    
    Je suis actuellement **disponible pour un entretien** afin de discuter de la manière dont je pourrais apporter de la valeur à votre organisation.
    
    N'hésitez pas à explorer les modules via le menu latéral 👈 ou à me contacter directement.
    """)
    
    
    st.markdown("### 🚀 Domaines d'Expertise")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("**🛡️ Solvabilité & Risques**\n\nMaîtrise approfondie de Solvabilité II (Piliers 1, 2, 3), ORSA, et des modèles de capital (SCR).")
        
    with col2:
        st.success("**📈 Finance & ALM**\n\nModélisation des actifs, couverture des risques financiers et optimisation de l'allocation d'actifs.")
        
    with col3:
        st.warning("**💻 Data & Tech**\n\nDéveloppement d'outils actuariels modernes en Python, automatisation et visualisation de données.")

    st.markdown("""
    ---
    #### 🛠 Stack Technique
    *   **Langage :** Python 3.10+
    *   **Interface :** Streamlit
    *   **Calculs :** NumPy, Pandas, Scipy
    *   **Visualisation :** Plotly Interactive
    """)
    

    # Ajout d'une section contact dans la sidebar pour le recrutement
    with st.sidebar:
        st.header("📬 Contact & Profil")
        st.markdown("Si ce profil vous intéresse pour une opportunité :")
        st.link_button("Mon Profil LinkedIn", "https://www.linkedin.com/in/nicolasrivollet/") # Remplacez par votre vrai lien si besoin
        st.link_button("Mon GitHub", "https://github.com/nicolasrivollet")

        # Bouton de téléchargement du CV
        cv_file = "cv_RivolletNicolas_v2602-5.pdf"
        if os.path.exists(cv_file):
            with open(cv_file, "rb") as pdf:
                st.download_button(label="📄 Télécharger mon CV", data=pdf, file_name="cv_RivolletNicolas_v2602-5.pdf", mime="application/pdf")

# Définition des objets pages
# Note : Pour l'accueil, on passe la fonction show_home au lieu du nom du fichier
home        = st.Page(show_home, title="Présentation", default=True,  icon="🏠")
normes      = st.Page("modules/normes_intro.py", title="Panorama des Normes Comptables", icon="📖")
nelson      = st.Page("modules/courbe_taux.py", title="Modèle Nelson-Siegel", icon="📈")
s2_piliers  = st.Page("modules/solvabilite2_piliers.py", title="Les 3 Piliers Solvabilité II", icon="🏛️")
comparat    = st.Page("modules/comparatif_modeles.py", title="Modélisation Courbe de Taux (intro)", icon="📊")
scr_screen  = st.Page("modules/scr_screener.py", title="SCR Asset Screener", icon="🔍")
smith       = st.Page("modules/smith_wilson.py", title="Modèle Smith-Wilson", icon="📐")
reform_s2   = st.Page("modules/reforme_s2.py", title="Réforme Solvabilité II", icon="⚖️")
archi_s2    = st.Page("modules/s2_architecture.py", title="Architecture Réglementaire", icon="🏢")
scr_global  = st.Page("modules/scr_standard.py", title="SCR Global (Agrégation)", icon="🔗")
cat_climat  = st.Page("modules/cat_nat_climat.py", title="Risque Climatique (Cat Nat)", icon="🌡️")
volat_adj   = st.Page("modules/volatility_adjustment.py", title="Volatility Adjustment", icon="⚙️")
chain_lad   = st.Page("modules/provisionnement_IARD.py", title="Chain-Ladder", icon="🔗")
scr_taux    = st.Page("modules/scr_taux.py", title="SCR Taux (Standard)", icon="💱")
reass_pilot = st.Page("modules/pilotage_reassu.py", title="Pilotage Réassurance", icon="🎯")
lee_carter  = st.Page("modules/mortalite_lee_carter.py", title="Mortalité (Lee-Carter)", icon="📉")
best_estim  = st.Page("modules/best_estimate_vie.py", title="Best Estimate Vie", icon="💰")
risk_dash   = st.Page("modules/dashboard_risques_financiers.py", title="Tableau de Bord Risques Financiers", icon="📊")
dora        = st.Page("modules/dora_regulation.py", title="Réglementation DORA", icon="🛡️")
gse         = st.Page("modules/gse_economique.py", title="Générateur Scénarios Eco (GSE)", icon="🎲")
data_qual   = st.Page("modules/data_quality_s2.py", title="Qualité des Données S2", icon="🗃️")
lux_vie     = st.Page("modules/luxembourg_vie.py", title="Assurance Vie Luxembourg", icon="🇱🇺")
esg_invest  = st.Page("modules/esg_investissements.py", title="ESG & Investissements", icon="🌿")
csrd        = st.Page("modules/csrd_reporting.py", title="Reporting CSRD", icon="🌱")
ifrs17      = st.Page("modules/ifrs17_csm.py", title="Moteur IFRS 17 (CSM)", icon="📊")
asset_class = st.Page("modules/asset_classes_risks.py", title="Classes d'Actifs & Risques", icon="💎")
risk_app    = st.Page("modules/risk_appetite.py", title="Appétence au Risque (RAF)", icon="🎯")
op_risk     = st.Page("modules/operational_risks.py", title="Risques Opérationnels", icon="🛠️")
orsa        = st.Page("modules/orsa_process.py", title="Processus ORSA", icon="🔄")
scr_lux     = st.Page("modules/scr_luxembourg.py", title="SCR Lux (Réassurance)", icon="🤝")
pdf_reader  = st.Page("modules/pdf_reader.py", title="Mon CV", icon="📄")
black_scholes = st.Page("modules/black_scholes.py", title="Modèle Black-Scholes", icon="📉")
ifrs9       = st.Page("modules/ifrs9_standard.py", title="Norme IFRS 9", icon="📉")
market_risk = st.Page("modules/market_risk_models.py", title="Modèles Risque Marché (VaR/IRC)", icon="📉")
glm_theory  = st.Page("modules/glm_theory.py", title="Théorie GLM", icon="📈")
alm_sim     = st.Page("modules/alm_simulator.py", title="Simulateur ALM (Fonds Euros)", icon="🏦")
pricing     = st.Page("modules/pricing_glm_xgb.py", title="Tarification (GLM vs ML)", icon="🤖")

# --- 3. NAVIGATION ---

# Dictionnaire complet des pages
pages = {
    "Accueil & Cadre Général": [home, normes, s2_piliers, archi_s2, lux_vie],
    "Modélisation Financière": [comparat, nelson, smith, gse, black_scholes, market_risk, glm_theory],
    "Risques & Allocation de Capital": [risk_dash, asset_class, scr_global, scr_taux, scr_screen, scr_lux],
    "Passif & Normes Comptables": [best_estim, alm_sim, pricing, ifrs17, ifrs9, reass_pilot],
    "Gouvernance & Prospective": [reform_s2, orsa, risk_app, op_risk, dora, csrd, data_qual, esg_invest, cat_climat],
}

# Ajout de la barre de recherche dans la sidebar
search_query = st.sidebar.text_input(
    "Filtrer les modules...",
    label_visibility="collapsed",
    placeholder="🔍 Ex: SCR, IFRS, Taux..."
)

# Logique de filtrage dynamique
if search_query:
    # On crée un nouveau dictionnaire pour les résultats
    filtered_pages = {}
    # On parcourt chaque catégorie et sa liste de pages
    for category, page_list in pages.items():
        # On ne garde que les pages dont le titre contient la recherche (insensible à la casse)
        matching_pages = [page for page in page_list if search_query.lower() in page.title.lower()]
        # Si on a trouvé des pages, on ajoute la catégorie et les pages correspondantes
        if matching_pages:
            filtered_pages[category] = matching_pages
    pg = st.navigation(filtered_pages)
else:
    # Si la barre de recherche est vide, on affiche le menu complet par défaut
    pg = st.navigation(pages)

# --- 4. EXÉCUTION ---
# pg.run() s'occupe de tout : 
# - Si home_page est sélectionnée, il exécute show_home()
# - Si une autre page est sélectionnée, il exécute le fichier .py correspondant
pg.run()