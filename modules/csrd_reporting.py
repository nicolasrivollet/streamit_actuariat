import streamlit as st
import pandas as pd

st.set_page_config(page_title="Reporting CSRD", layout="wide")

st.title("🌱 CSRD : Corporate Sustainability Reporting Directive")
st.subheader("La révolution du reporting extra-financier")

st.markdown("""
La **CSRD (Corporate Sustainability Reporting Directive)** remplace la NFRD et impose aux entreprises de publier des informations détaillées sur leurs risques, opportunités et impacts liés aux questions **ESG** (Environnement, Social, Gouvernance).
Son objectif est de mettre l'information extra-financière sur le même plan que l'information financière.
""")

st.divider()

# --- 1. DOUBLE MATÉRIALITÉ ---
st.header("1. Le Concept Clé : La Double Matérialité")
st.markdown("C'est la pierre angulaire de la CSRD. Une entreprise doit reporter sur un sujet s'il est matériel selon l'une des deux perspectives (ou les deux).")

col1, col2 = st.columns(2)

with col1:
    st.info("### 🌍 Matérialité d'Impact (Inside-Out)")
    st.markdown("""
    **L'impact de l'entreprise sur le monde.**
    *   Quels sont les impacts (positifs ou négatifs) de mes activités sur l'environnement et la société ?
    *   *Exemple Assurance :* Empreinte carbone du portefeuille d'investissement, politique de souscription (exclusion du charbon).
    """)

with col2:
    st.warning("### 💰 Matérialité Financière (Outside-In)")
    st.markdown("""
    **L'impact du monde sur l'entreprise.**
    *   Comment les enjeux de durabilité influencent-ils ma performance financière, mes flux de trésorerie ou mon accès au capital ?
    *   *Exemple Assurance :* Coût des sinistres climatiques (Cat Nat), risque de transition sur les actifs échoués (Stranded Assets).
    """)

st.divider()

# --- 2. LES NORMES ESRS ---
st.header("2. Les Normes ESRS (European Sustainability Reporting Standards)")
st.markdown("Le contenu du rapport est standardisé par l'EFRAG à travers 12 normes sectorielles agnostiques.")

tab1, tab2, tab3, tab4 = st.tabs(["Transverses", "Environnement (E)", "Social (S)", "Gouvernance (G)"])

with tab1:
    st.markdown("""
    *   **ESRS 1 (Exigences générales) :** Principes de reporting (double matérialité, chaîne de valeur).
    *   **ESRS 2 (Informations générales) :** Gouvernance, stratégie, gestion des impacts, risques et opportunités. **(Obligatoire pour tous)**
    """)

with tab2:
    st.markdown("""
    *   **ESRS E1 (Changement climatique) :** Émissions GES (Scopes 1, 2, 3), adaptation, atténuation.
    *   **ESRS E2 (Pollution)**
    *   **ESRS E3 (Ressources aquatiques et marines)**
    *   **ESRS E4 (Biodiversité et écosystèmes)**
    *   **ESRS E5 (Utilisation des ressources et économie circulaire)**
    """)

with tab3:
    st.markdown("""
    *   **ESRS S1 (Effectifs propres) :** Conditions de travail, égalité, diversité.
    *   **ESRS S2 (Travailleurs de la chaîne de valeur)**
    *   **ESRS S3 (Communautés affectées)**
    *   **ESRS S4 (Consommateurs et utilisateurs finaux)**
    """)

with tab4:
    st.markdown("""
    *   **ESRS G1 (Conduite des affaires) :** Culture d'entreprise, protection des lanceurs d'alerte, corruption, paiement des fournisseurs.
    """)

st.divider()

# --- 3. IMPACT POUR L'ACTUAIRE ---
st.header("3. Implications pour l'Actuaire & le Risk Manager")

with st.expander("📊 Qualité de la Donnée & Audit", expanded=True):
    st.write("""
    Le rapport CSRD doit être **audité** (assurance limitée puis raisonnable).
    Cela impose aux actuaires de structurer la collecte de données ESG (ex: émissions carbone des actifs) avec la même rigueur que les données financières (Solvabilité II).
    """)

with st.expander("🔗 Lien avec Solvabilité II (ORSA)", expanded=True):
    st.write("""
    L'analyse de matérialité financière de la CSRD nourrit directement l'**ORSA** (Own Risk and Solvency Assessment).
    Les scénarios climatiques utilisés pour la CSRD (ESRS E1) doivent être cohérents avec ceux utilisés pour les stress-tests prudentiels.
    """)

with st.expander("🎯 Stratégie & Souscription", expanded=True):
    st.write("""
    La publication d'indicateurs clés (KPIs) comme la "Part verte" (Taxonomie) ou l'intensité carbone oblige à revoir la stratégie d'investissement et de souscription pour atteindre les objectifs affichés (Plan de Transition).
    """)

st.divider()
st.caption("Référence : Directive (UE) 2022/2464 (CSRD)")