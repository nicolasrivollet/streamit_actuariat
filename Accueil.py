import streamlit as st
import os
from modules.ui_theme import apply_theme

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Portfolio Actuariat & Risques",
    page_icon="📊",
    layout="wide"
)

# Application globale de la charte graphique institutionnelle
apply_theme()

# --- 2. DÉFINITION DES PAGES ---

# La page d'accueil pointe vers une fonction interne ou le fichier lui-même
def show_home():
    st.title("Nicolas Rivollet")
    st.subheader("Actuariat, Modélisation Financière et Gestion des Risques")
    
    st.markdown("""
    Bienvenue sur ce portail professionnel. Cet espace interactif regroupe des outils de modélisation quantitative, 
    des simulateurs prudentiels et des tableaux de bord conçus pour illustrer la mise en pratique de compétences avancées en 
    **actuariat**, **gestion des risques** et **data science**.
    """)
    
    st.markdown("### Domaines d'Expertise")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="exec-card">
            <div class="exec-card-title">Solvabilité & Réglementation</div>
            <div class="exec-card-text">
                Maîtrise approfondie des cadres prudentiels : Solvabilité II (Piliers 1, 2 et 3), modélisation et calcul du SCR (formule standard et chocs), processus ORSA, revue 2020 et normes comptables (IFRS 17, IFRS 9, French GAAP).
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="exec-card">
            <div class="exec-card-title">Finance & Gestion Actif-Passif</div>
            <div class="exec-card-text">
                Modélisation des taux d'intérêt (Nelson-Siegel, Smith-Wilson), valorisation d'options financières (Black-Scholes), Générateur de Scénarios Économiques (GSE), simulation ALM (fonds en euros) et optimisation de l'allocation d'actifs.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="exec-card">
            <div class="exec-card-title">Passif, Data Science & Tech</div>
            <div class="exec-card-text">
                Méthodes de provisionnement IARD (Chain-Ladder, IBNR), tables de mortalité stochastiques (Lee-Carter), tarification actuarielle (GLM vs Machine Learning) et gouvernance des risques émergents (DORA, CSRD, Cat Nat).
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Environnement Technique")
    st.markdown("""
    <div style="margin-top: 0.5rem; margin-bottom: 1.5rem;">
        <span class="badge-pill">Python 3.11</span>
        <span class="badge-pill">Streamlit</span>
        <span class="badge-pill">NumPy & Pandas</span>
        <span class="badge-pill">SciPy Optimization</span>
        <span class="badge-pill">Plotly Interactive</span>
        <span class="badge-pill">Scikit-Learn</span>
        <span class="badge-pill">ChainLadder</span>
        <span class="badge-pill">Smith-Wilson Engine</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Contact & Échange")
    st.markdown("""
    Disponible pour échanger sur des opportunités professionnelles ou des missions de conseil dans les domaines de l'actuariat, de la modélisation financière et du risk management.
    """)
    st.link_button("Consulter mon profil LinkedIn", "https://www.linkedin.com/in/nicolasrivollet/")

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
black_scholes = st.Page("modules/black_scholes.py", title="Modèle Black-Scholes", icon="📉")
ifrs9       = st.Page("modules/ifrs9_standard.py", title="Norme IFRS 9", icon="📉")
market_risk = st.Page("modules/market_risk_models.py", title="Modèles Risque Marché (VaR/IRC)", icon="📉")
glm_theory  = st.Page("modules/glm_theory.py", title="Théorie GLM", icon="📈")
alm_sim     = st.Page("modules/alm_simulator.py", title="Simulateur ALM (Fonds Euros)", icon="🏦")
uc_select   = st.Page("modules/uc_selection.py", title="Sélection Supports UC", icon="✅")
pricing     = st.Page("modules/pricing_glm_xgb.py", title="Tarification (GLM vs ML)", icon="🤖")
proba_dist  = st.Page("modules/proba_distributions.py", title="Lois de Probabilités", icon="🎲")

# --- 3. NAVIGATION ---

# Dictionnaire complet des pages
pages = {
    "Accueil & Cadre Général": [home, normes, s2_piliers, archi_s2, lux_vie],
    "Modélisation Financière": [comparat, nelson, smith, gse, black_scholes, market_risk, glm_theory, proba_dist],
    "Risques & Allocation de Capital": [risk_dash, asset_class, scr_global, scr_taux, scr_screen, uc_select, scr_lux],
    "Gouvernance & Prospective": [reform_s2, orsa, risk_app, op_risk, dora, csrd, data_qual, esg_invest, cat_climat],
}

pg = st.navigation(pages)

# --- 4. EXÉCUTION ---
# pg.run() s'occupe de tout : 
# - Si home_page est sélectionnée, il exécute show_home()
# - Si une autre page est sélectionnée, il exécute le fichier .py correspondant
pg.run()