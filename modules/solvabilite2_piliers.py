import streamlit as st
import pandas as pd

st.set_page_config(page_title="Les 3 Piliers Solvabilité II", layout="wide")

st.title("🏛️ Solvabilité II : Les 3 Piliers")
st.subheader("Une approche fondée sur les risques (Risk-Based Approach)")

st.markdown("""
La directive Solvabilité II repose sur une architecture en trois piliers, inspirée des accords de Bâle II pour les banques.
Elle ne se limite pas à des calculs de capital (Pilier 1), mais impose également une gouvernance stricte (Pilier 2) et une transparence accrue (Pilier 3).
""")

st.divider()

# --- NAVIGATION ---
tab1, tab2, tab3 = st.tabs(["📊 Pilier 1 : Quantitatif", "⚖️ Pilier 2 : Gouvernance", "📢 Pilier 3 : Reporting"])

# --- PILIER 1 ---
with tab1:
    st.header("Pilier 1 : Exigences Quantitatives")
    st.markdown("""
    Ce pilier définit les règles de valorisation du bilan et de calcul du capital.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. Le Bilan Économique")
        st.info("""
        **Market Consistent Balance Sheet (MCBS)**
        *   **Actifs :** Valorisés à la "Juste Valeur" (Fair Value / Mark-to-Market).
        *   **Passifs :** Best Estimate (Flux actualisés) + Marge de Risque.
        *   **Fonds Propres (Own Funds) :** L'excédent d'Actif sur le Passif, classé en Tiers (1, 2, 3) selon leur qualité (permanence, subordination).
        """)
        
    with col2:
        st.subheader("2. Les Exigences de Capital")
        st.warning("""
        **SCR (Solvency Capital Requirement) :**
        *   Capital nécessaire pour absorber un choc bicentenaire (VaR 99.5% à 1 an).
        *   Si Fonds Propres < SCR : Intervention du régulateur, plan de rétablissement.
        
        **MCR (Minimum Capital Requirement) :**
        *   Seuil de solvabilité ultime (généralement entre 25% et 45% du SCR).
        *   Si Fonds Propres < MCR : Retrait d'agrément potentiel.
        """)

    st.markdown("---")
    st.subheader("Architecture du SCR (Formule Standard)")
    st.markdown("Le SCR est modulaire. Il agrège différents risques via une matrice de corrélation.")
    
    # Petit diagramme ou texte structuré
    st.markdown("""
    *   **Risque de Marché :** Taux, Actions, Immobilier, Spread, Change, Concentration.
    *   **Risque de Souscription (Vie/Non-Vie/Santé) :** Mortalité, Longevité, Catastrophe, Rachats.
    *   **Risque de Contrepartie :** Défaut des réassureurs ou banques.
    *   **Risque Opérationnel :** Défaillance des processus ou systèmes.
    """)

# --- PILIER 2 ---
with tab2:
    st.header("Pilier 2 : Gouvernance et Supervision")
    st.markdown("""
    Ce pilier impose aux assureurs de mettre en place un système de gestion des risques robuste.
    Il ne suffit pas d'avoir du capital, il faut savoir piloter l'entreprise.
    """)
    
    col_gov1, col_gov2 = st.columns(2)
    
    with col_gov1:
        st.subheader("1. Les 4 Fonctions Clés")
        st.write("Elles doivent être indépendantes et avoir un accès direct au Conseil d'Administration (AMSB).")
        st.success("""
        1.  **Fonction Gestion des Risques :** Cartographie, surveillance et reporting des risques.
        2.  **Fonction Actuarielle :** Avis sur la souscription, la réassurance et le calcul des provisions techniques.
        3.  **Fonction Conformité (Compliance) :** Respect des lois et normes (interne/externe).
        4.  **Fonction Audit Interne :** Contrôle périodique de l'efficacité du système.
        """)
        
    with col_gov2:
        st.subheader("2. ORSA (Auto-évaluation)")
        st.write("**Own Risk and Solvency Assessment**")
        st.info("""
        C'est le cœur du Pilier 2. L'assureur doit évaluer ses propres besoins de solvabilité, au-delà de la formule standard.
        *   Vision prospective (3-5 ans).
        *   Lien avec la stratégie commerciale (Business Plan).
        *   Stress-tests spécifiques (ex: Climat, Inflation).
        """)

    st.markdown("---")
    st.subheader("Principe de la Personne Prudente")
    st.write("L'assureur est libre d'investir dans les actifs de son choix (fin des quotas d'investissement), à condition de pouvoir **identifier, mesurer, surveiller et gérer** les risques associés. On ne doit investir que dans ce que l'on comprend.")

# --- PILIER 3 ---
with tab3:
    st.header("Pilier 3 : Discipline de Marché (Reporting)")
    st.markdown("""
    L'objectif est d'assurer la transparence vis-à-vis du public et du superviseur (ACPR en France).
    """)
    
    st.table(pd.DataFrame({
        "Rapport": ["SFCR (Solvency and Financial Condition Report)", "RSR (Regular Supervisory Report)", "QRT (Quantitative Reporting Templates)"],
        "Destinataire": ["Grand Public (Site Web)", "Superviseur (ACPR)", "Superviseur (ACPR)"],
        "Fréquence": ["Annuel", "Tous les 3 ans (ou annuel si demandé)", "Trimestriel & Annuel"],
        "Contenu": ["Chiffres clés, Gouvernance, Profil de risque, Gestion du capital.", "Détails stratégiques confidentiels, Analyse approfondie.", "Tableaux de données standardisés (centaines de cellules XML)."]
    }))
    
    st.info("💡 **Enjeu Data :** La production des QRT (états S.06.02 sur les actifs, S.23.01 sur les fonds propres...) est un défi industriel pour les assureurs, nécessitant des outils de Data Quality puissants.")

st.divider()
st.caption("Référence : Directive 2009/138/CE (Solvabilité II)")