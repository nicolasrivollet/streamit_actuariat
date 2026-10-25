import streamlit as st
import pandas as pd

st.set_page_config(page_title="Réglementation DORA", layout="wide")

st.title("DORA : Digital Operational Resilience Act")
st.subheader("Règlement (UE) 2022/2554 sur la résilience opérationnelle numérique")

st.markdown("""
**DORA** est le nouveau cadre réglementaire européen visant à renforcer la sécurité informatique du secteur financier.
Contrairement à Solvabilité II qui exige des fonds propres pour absorber les pertes, DORA exige des **capacités opérationnelles** pour résister, répondre et se rétablir face aux cyberattaques.

📅 **Entrée en application :** 17 janvier 2025.
""")

st.divider()

# --- LES 5 PILIERS ---
st.header("Les 5 Piliers de DORA")
st.markdown("Le règlement s'articule autour de cinq domaines clés pour assurer une hygiène numérique complète.")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1. Gestion des Risques TIC", 
    "2. Gestion des Incidents", 
    "3. Tests de Résilience", 
    "4. Risque Tiers (Fournisseurs)", 
    "5. Partage d'Information"
])

with tab1:
    st.subheader("1. Gestion des Risques TIC (ICT Risk Management)")
    st.markdown("""
    C'est la fondation. Les entités financières doivent avoir un cadre de gouvernance et de contrôle interne robuste.
    
    *   **Responsabilité :** L'organe de direction (Conseil d'Administration) est *in fine* responsable de la gestion du risque cyber. Il doit être formé à ces enjeux.
    *   **Cadre de gestion :** Identification, Protection, Détection, Réponse et Rétablissement (proche du framework NIST).
    *   **Actifs :** Cartographie précise et à jour des actifs informatiques critiques.
    """)
    st.info("**Changement de paradigme :** Le risque cyber n'est plus un sujet 'IT' délégué au DSI, mais un sujet 'Stratégique' piloté par la Direction Générale.")

with tab2:
    st.subheader("2. Gestion et Notification des Incidents")
    st.markdown("""
    L'objectif est d'harmoniser la remontée d'informations vers les superviseurs pour avoir une vision systémique des attaques.
    
    *   **Classification :** Critères stricts pour définir ce qu'est un "incident majeur" (impact financier, nombre de clients touchés, durée, perte de données).
    *   **Reporting :** Obligation de notifier les incidents majeurs aux autorités compétentes (ACPR/BCE) dans des délais très courts.
        *   *Notification initiale* (dès détection).
        *   *Rapport intermédiaire* (pendant la crise).
        *   *Rapport final* (avec analyse des causes racines - RCA).
    """)

with tab3:
    st.subheader("3. Tests de Résilience Opérationnelle")
    st.markdown("""
    Il ne suffit pas de dire qu'on est sécurisé, il faut le prouver par l'attaque.
    
    *   **Tests basiques (Annuels) :** Scans de vulnérabilité, tests d'intrusion classiques, analyses de code source.
    *   **TLPT (Threat-Led Penetration Testing) :** Pour les entités importantes, obligation de réaliser tous les 3 ans un test d'intrusion avancé ("Red Teaming") simulant une attaque réelle sur les systèmes de production (Live).
    """)
    st.warning("⚠️ **Challenge :** Tester sur la production sans causer d'incident réel demande une maturité technique extrême.")

with tab4:
    st.subheader("4. Gestion des Risques Tiers (Third-Party Risk)")
    st.markdown("""
    Les assureurs dépendent de plus en plus du Cloud (AWS, Azure, Google) et de fournisseurs SaaS. DORA encadre cette dépendance critique.
    
    *   **Registre d'Information :** Tenue d'un registre exhaustif de tous les contrats de sous-traitance TIC.
    *   **Clauses contractuelles :** Droit d'audit, localisation des données, niveaux de service (SLA) garantis, stratégie de sortie (réversibilité).
    *   **Supervision directe :** Les "Prestataires Tiers Critiques" (CTPP) seront directement surveillés par les autorités européennes (ESA).
    """)

with tab5:
    st.subheader("5. Partage d'Information")
    st.markdown("""
    DORA encourage les institutions financières à s'unir face aux attaquants.
    
    *   **Cyber Threat Intelligence (CTI) :** Possibilité d'échanger des indicateurs de compromission (IoC), des tactiques et des procédures entre acteurs financiers, via des plateformes sécurisées, sans violer le RGPD ou le secret des affaires.
    """)

st.divider()

# --- IMPACT ACTUARIEL ---
st.header("Pourquoi cela concerne l'Actuaire / Risk Manager ?")

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("### 1. Risque Opérationnel (S2)")
    st.write("""
    Le risque cyber est une composante majeure du **Risque Opérationnel** dans Solvabilité II.
    DORA fournit le cadre pour mieux :
    *   **Identifier** les scénarios de risques extrêmes (pour l'ORSA).
    *   **Quantifier** l'impact financier potentiel d'une interruption d'activité (perte de CA, frais de remédiation, amendes).
    *   **Justifier** les mesures de réduction du risque (mitigation) dans le calcul du capital.
    """)

with col_b:
    st.markdown("### 2. Cyber-Assurance (Souscription)")
    st.write("""
    Pour les actuaires qui tarifient des produits de **Cyber-Assurance**, DORA est une bénédiction :
    *   Elle standardise le niveau de sécurité des clients (s'ils sont financiers).
    *   Elle fournit des données d'incidents plus structurées pour calibrer les modèles de fréquence/coût.
    *   Elle réduit l'asymétrie d'information entre l'assureur et l'assuré.
    """)

st.divider()
st.caption("Source : Règlement (UE) 2022/2554 du Parlement européen et du Conseil du 14 décembre 2022.")