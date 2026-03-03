import streamlit as st
import inspect
from pathlib import Path

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
    """)

    st.info("👈 **Utilisez le menu latéral pour naviguer à travers les différents modules de modélisation.**")

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
        st.markdown("---")
        st.header("📬 Contact & Profil")
        st.markdown("Si ce profil vous intéresse pour une opportunité :")
        st.link_button("Mon Profil LinkedIn", "https://www.linkedin.com/in/nicolasrivollet/") # Remplacez par votre vrai lien si besoin
        st.link_button("Mon GitHub", "https://github.com/nicolasrivollet")

        # Bouton de téléchargement du CV
        import os
        cv_file = "cv_RivolletNicolas_v2602-5.pdf"
        if os.path.exists(cv_file):
            with open(cv_file, "rb") as pdf:
                st.download_button(label="📄 Télécharger mon CV", data=pdf, file_name="cv_RivolletNicolas_v2602-5.pdf", mime="application/pdf")

# --- INDEXATION POUR RECHERCHE ---
search_index = {}

def create_page(source, **kwargs):
    """Crée une page Streamlit et indexe son contenu pour la recherche."""
    page = st.Page(source, **kwargs)
    
    # Extraction du contenu pour l'indexation
    content = ""
    if isinstance(source, str):
        try:
            # Lecture du fichier source
            content = Path(source).read_text(encoding="utf-8")
        except Exception:
            pass
    elif callable(source):
        try:
            # Lecture du code de la fonction
            content = inspect.getsource(source)
        except Exception:
            pass
            
    # Stockage : Titre + Contenu (en minuscule pour recherche insensible à la casse)
    title = kwargs.get("title", "").lower()
    search_index[page] = f"{title} {content.lower()}"
    
    return page

# --- DÉFINITION DES PAGES (Avec Indexation) ---
home        = create_page(show_home, title="Présentation", default=True,  icon="🏚️")
normes      = create_page("modules/normes_intro.py", title="Panorama des Normes Comptables", icon="📖")
nelson      = create_page("modules/courbe_taux.py", title="Modèle Nelson-Siegel", icon="📈")
s2_piliers  = create_page("modules/solvabilite2_piliers.py", title="Les 3 Piliers Solvabilité II", icon="🏛️")
comparat    = create_page("modules/comparatif_modeles.py", title="Modélisation Courbe de Taux (intro)", icon="📊")
scr_screen  = create_page("modules/scr_screener.py", title="SCR Asset Screener", icon="🔍")
smith       = create_page("modules/smith_wilson.py", title="Modèle Smith-Wilson", icon="📐")
reform_s2   = create_page("modules/reforme_s2.py", title="Réforme Solvabilité II", icon="⚖️")
archi_s2    = create_page("modules/s2_architecture.py", title="Architecture Réglementaire", icon="🏢")
scr_global  = create_page("modules/scr_standard.py", title="SCR Global (Agrégation)", icon="🔗")
cat_climat  = create_page("modules/cat_nat_climat.py", title="Risque Climatique (Cat Nat)", icon="🌡️")
volat_adj   = create_page("modules/volatility_adjustment.py", title="Volatility Adjustment", icon="⚙️")
chain_lad   = create_page("modules/provisionnement_IARD.py", title="Chain-Ladder", icon="🔗")
scr_taux    = create_page("modules/scr_taux.py", title="SCR Taux (Standard)", icon="💱")
reass_pilot = create_page("modules/pilotage_reassu.py", title="Pilotage Réassurance", icon="🎯")
lee_carter  = create_page("modules/mortalite_lee_carter.py", title="Mortalité (Lee-Carter)", icon="�")
best_estim  = create_page("modules/best_estimate_vie.py", title="Best Estimate Vie", icon="💰")
risk_dash   = create_page("modules/dashboard_risques_financiers.py", title="Tableau de Bord Risques Financiers", icon="📊")
dora        = create_page("modules/dora_regulation.py", title="Réglementation DORA", icon="🛡️")
gse         = create_page("modules/gse_economique.py", title="Générateur Scénarios Eco (GSE)", icon="🎲")
data_qual   = create_page("modules/data_quality_s2.py", title="Qualité des Données S2", icon="🗃️")
lux_vie     = create_page("modules/luxembourg_vie.py", title="Assurance Vie Luxembourg", icon="🇱🇺")
esg_invest  = create_page("modules/esg_investissements.py", title="ESG & Investissements", icon="🌿")
csrd        = create_page("modules/csrd_reporting.py", title="Reporting CSRD", icon="🌱")
ifrs17      = create_page("modules/ifrs17_csm.py", title="Moteur IFRS 17 (CSM)", icon="📊")
asset_class = create_page("modules/asset_classes_risks.py", title="Classes d'Actifs & Risques", icon="💎")
risk_app    = create_page("modules/risk_appetite.py", title="Appétence au Risque (RAF)", icon="🎯")
op_risk     = create_page("modules/operational_risks.py", title="Risques Opérationnels", icon="🛠️")
orsa        = create_page("modules/orsa_process.py", title="Processus ORSA", icon="🔄")
scr_lux     = create_page("modules/scr_luxembourg.py", title="SCR Lux (Réassurance)", icon="🤝")
pdf_reader  = create_page("modules/pdf_reader.py", title="Mon CV", icon="📄")
bale3       = create_page("modules/bale3_regulation.py", title="Réglementation Bâle III", icon="🏦")
black_scholes = create_page("modules/black_scholes.py", title="Modèle Black-Scholes", icon="📉")
ifrs9       = create_page("modules/ifrs9_standard.py", title="Norme IFRS 9", icon="📉")
market_risk = create_page("modules/market_risk_models.py", title="Modèles Risque Marché (VaR/IRC)", icon="📉")

# --- 3. NAVIGATION ---

# Dictionnaire complet des pages
pages = {
    "🏠 Présentation & Cadre": [home, normes, ifrs9, s2_piliers, bale3, archi_s2, pdf_reader],
    "⚖️ Focus Réglementaire & ESG": [reform_s2, orsa, risk_app, op_risk, dora, csrd, data_qual, esg_invest, cat_climat],
    "📈 Finance & Actif": [risk_dash, asset_class, market_risk, gse, black_scholes, scr_screen, scr_taux, volat_adj, comparat, nelson, smith],
    "🛡️ Passif & Solvabilité": [best_estim, ifrs17, lee_carter, lux_vie, scr_lux, chain_lad, reass_pilot, scr_global],
}

# Ajout de la barre de recherche dans la sidebar
st.markdown("---")
search_query = st.sidebar.text_input(
    "Filtrer les modules...",
    label_visibility="collapsed",
    placeholder="🔍 Ex: SCR, IFRS, Taux..."
)

# Logique de filtrage dynamique
if search_query:
    query = search_query.lower()
    # On crée un nouveau dictionnaire pour les résultats
    filtered_pages = {}
    # On parcourt chaque catégorie et sa liste de pages
    for category, page_list in pages.items():
        # On garde les pages si la recherche est dans l'index (Titre ou Contenu)
        matching_pages = [page for page in page_list if query in search_index.get(page, "")]
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