import streamlit as st
import pandas as pd

st.set_page_config(page_title="Assurance Vie Luxembourg", layout="wide")

st.title("Assurance Vie Luxembourg : Spécificités & Risques")
st.subheader("Le Triangle de Sécurité et la Gestion de Fortune (Wealth Insurance)")

st.markdown("""
Le Luxembourg est le hub européen de l'assurance-vie en **Libre Prestation de Services (LPS)**. 
Pour un Risk Manager, ce marché se distingue par son cadre de protection des actifs unique (**Triangle de Sécurité**) et la sophistication de ses véhicules d'investissement (**FID, FAS**), souvent utilisés pour la planification successorale des **HNWI** (High Net Worth Individuals).
""")

st.divider()

# --- 1. LE CADRE DE PROTECTION ---
st.header("1. Le Triangle de Sécurité & Super Privilège")
st.markdown("Le Luxembourg offre le niveau de protection des souscripteurs le plus élevé d'Europe.")

col1, col2 = st.columns(2)

with col1:
    st.info("### Le Triangle de Sécurité")
    st.markdown("""
    Mécanisme de contrôle strict imposé par le **Commissariat aux Assurances (CAA)**.
    Il impose la signature d'une convention tripartite entre :
    1.  **L'Assureur**
    2.  **La Banque Dépositaire** (qui doit être agréée et séparée)
    3.  **Le Régulateur (CAA)**
    
    **Conséquence :** Les actifs des clients (Provisions Techniques) sont ségrégués des fonds propres de l'assureur et déposés sur des comptes bancaires distincts. Le CAA peut geler ces comptes directement.
    """)

with col2:
    st.success("### Le Super Privilège")
    st.markdown("""
    En cas de défaillance de l'assureur, la loi luxembourgeoise accorde aux souscripteurs un **privilège absolu de premier rang**.
    
    *   **Priorité :** Les clients passent avant tous les autres créanciers (État, Trésor Public, Salariés, Actionnaires).
    *   **Universalité :** Ce privilège s'applique à l'ensemble des actifs représentatifs des provisions techniques.
    """)

st.divider()

# --- 2. LES VÉHICULES D'INVESTISSEMENT ---
st.header("2. La Circulaire 15/3 : Flexibilité d'Investissement")
st.markdown("""
Contrairement aux contrats standards, le Luxembourg permet d'investir dans des actifs très variés (Private Equity, Immobilier, Titres non cotés) via des fonds dédiés, selon la classification du client.
""")

# Classification des souscripteurs
st.markdown("#### 📊 Classification des Souscripteurs (N, A, B, C, D)")
st.write("L'univers d'investissement dépend de la fortune mobilière du client et du montant investi.")

cols = st.columns(5)
cols[0].metric("Catégorie N", "< 250 k€", "Fonds Standards")
cols[1].metric("Catégorie A", "> 250 k€", "Fonds Externes")
cols[2].metric("Catégorie B", "> 500 k€", "+ FID (Gestion discrétionnaire)")
cols[3].metric("Catégorie C", "> 1.25 M€", "+ FAS (Produits structurés)")
cols[4].metric("Catégorie D", "> 2.5 M€", "+ Private Equity / Non Coté")

# Tableau des fonds
st.markdown("#### 🛠️ Typologie des Fonds")
data_fonds = {
    "Type de Fonds": ["Fonds Général", "Fonds Interne Collectif (FIC)", "Fonds Interne Dédié (FID)", "Fonds d'Assurance Spécialisé (FAS)"],
    "Définition": ["Actif général de l'assureur avec garantie (rare en Lux).", "Fonds ouvert à une multitude de clients (profilé).", "Fonds géré pour UN client par un gestionnaire financier agréé.", "Fonds sans gestionnaire (Buy & Hold), le client choisit ses actifs."],
    "Risque pour l'Assureur": ["Risque de marché & crédit (Bilan)", "Risque opérationnel (NAV)", "Risque de conformité (Actifs éligibles)", "Risque de valorisation (Illiquides)"]
}
st.table(pd.DataFrame(data_fonds))

st.divider()

# --- 3. VISION HEAD OF RISK ---
st.header("3. Les Défis du Risk Management au Luxembourg")
st.markdown("Le modèle luxembourgeois engendre une cartographie des risques spécifique.")

with st.expander("🌍 Risque Juridique & Cross-Border (LPS)", expanded=True):
    st.write("""
    L'assureur opère dans plusieurs pays (France, Italie, Belgique, etc.).
    *   **Droit du contrat :** Il faut respecter le Code des Assurances du pays de résidence du client (ex: Loi Sapin 2 en France, Code civil italien).
    *   **Fiscalité :** Prélèvement à la source spécifique par pays.
    *   **Veille réglementaire :** Le Risk Manager doit surveiller les évolutions légales dans 10+ juridictions simultanément.
    """)

with st.expander("🕵️ Risque de Conformité & AML/CFT", expanded=True):
    st.write("""
    La clientèle HNWI (High Net Worth Individuals) présente un profil de risque élevé.
    *   **Origine des fonds :** Structures complexes (Trusts, Holdings, SPF).
    *   **PPE :** Personnes Politiquement Exposées.
    *   **Sanctions internationales :** Filtrage strict des bénéficiaires effectifs (UBO).
    """)

with st.expander("📉 Risque de Marché & Valorisation (Actifs Illiquides)", expanded=True):
    st.write("""
    Dans les FAS (Fonds d'Assurance Spécialisés), les clients logent souvent des actifs non cotés (Private Equity, Dette privée).
    *   **Challenge :** Obtenir une valorisation fiable et fréquente pour le calcul de la NAV et du SCR.
    *   **Look-through :** Obligation de "transpariser" les fonds pour calculer le SCR Marché réel (et non le choc forfaitaire "Type 2").
    """)