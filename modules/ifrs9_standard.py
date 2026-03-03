import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Norme IFRS 9", layout="wide")

st.title("📉 IFRS 9 : Instruments Financiers")
st.subheader("La révolution du provisionnement pour risque de crédit")

st.markdown("""
La norme **IFRS 9**, qui a remplacé IAS 39, a introduit des changements fondamentaux dans la comptabilisation des instruments financiers.
Ses trois piliers sont :
1.  **Classification & Mesure :** Comment classer et valoriser les actifs financiers.
2.  **Dépréciation (Impairment) :** Le passage d'un modèle de **pertes avérées** à un modèle de **pertes attendues (ECL)**.
3.  **Comptabilité de Couverture (Hedge Accounting) :** Un alignement plus étroit avec la gestion des risques.
""")

st.divider()

# --- 1. CLASSIFICATION & MESURE ---
st.header("1. Classification & Mesure")
st.markdown("""
La classification d'un actif financier dépend de deux tests :
*   **Test SPPI (Solely Payments of Principal and Interest) :** Les flux de trésorerie contractuels de l'actif sont-ils uniquement des paiements de principal et d'intérêts ? (Un prêt classique passe le test, une action non).
*   **Test du Business Model :** Quel est l'objectif de l'entité ? Détenir l'actif pour encaisser les flux (Hold to Collect), le vendre (Hold to Sell), ou les deux ?
""")

# Simple diagram
st.image("https://www.ey.com/en_gl/ifrs-technical-resources/a-practical-guide-to-ifrs-9-s-financial-instrument-classification-and-measurement-requirements/_jcr_content/image.coreimg.82.1280.png/1627568400490.png", caption="Arbre de décision IFRS 9 (Source: EY)")

tab_class1, tab_class2, tab_class3 = st.tabs(["Amortised Cost (AC)", "FVOCI", "FVTPL"])

with tab_class1:
    st.info("### Coût Amorti (Amortised Cost)")
    st.write("**Condition :** SPPI OK + Business Model = Hold to Collect.")
    st.write("**Traitement :** L'actif est valorisé à son coût initial, ajusté des remboursements et d'un amortissement de la prime/décote (méthode du Taux d'Intérêt Effectif - TIE). Les variations de juste valeur sont ignorées.")
    st.caption("Exemple typique : Portefeuille de prêts bancaires classiques.")

with tab_class2:
    st.warning("### Juste Valeur par OCI (Fair Value through OCI)")
    st.write("**Condition :** SPPI OK + Business Model = Hold to Collect and Sell.")
    st.write("**Traitement :** L'actif est au bilan à sa juste valeur. Les variations de juste valeur sont enregistrées en **OCI (Autres Éléments du Résultat Global)**, sans impacter le P&L, jusqu'à la cession de l'actif.")
    st.caption("Exemple typique : Portefeuille obligataire de liquidité d'un assureur.")

with tab_class3:
    st.error("### Juste Valeur par P&L (Fair Value through P&L)")
    st.write("**Condition :** Tous les autres cas (actions, dérivés, ou option FVTPL).")
    st.write("**Traitement :** L'actif est au bilan à sa juste valeur. Toutes les variations de juste valeur impactent **directement le compte de résultat (P&L)**.")
    st.caption("Exemple typique : Portefeuille d'actions de trading.")

st.divider()

# --- 2. IMPAIRMENT (ECL) ---
st.header("2. Dépréciation : Le Modèle des Pertes Attendues (ECL)")
st.markdown("""
C'est le changement le plus structurant. Fini d'attendre un événement de perte avéré (défaut) pour provisionner.
Dès l'origine, il faut provisionner les pertes de crédit **attendues**. Le modèle se base sur 3 "buckets" (étapes).
""")

col_ecl1, col_ecl2 = st.columns([1, 2])

with col_ecl1:
    st.subheader("Les 3 Étapes du Modèle ECL")
    st.success("**Étape 1 (Performing) :**\nPour les actifs performants, on provisionne les pertes de crédit attendues à **12 mois** (12-month ECL).")
    st.warning("**Étape 2 (Underperforming) :**\nSi le risque de crédit a **augmenté de manière significative (SICR)**, on provisionne les pertes attendues sur **toute la durée de vie** de l'actif (Lifetime ECL).")
    st.error("**Étape 3 (Non-Performing) :**\nSi l'actif est déprécié (en défaut), on provisionne également les **Lifetime ECL**, mais le calcul des intérêts se fait sur la base du montant net de provision.")

with col_ecl2:
    st.subheader("Simulateur de Provisionnement ECL")
    
    exposure = 1000
    pd_12m = st.slider("PD à 12 mois (%)", 0.1, 5.0, 1.0) / 100
    lgd_ecl = st.slider("LGD (%)", 10.0, 100.0, 40.0) / 100
    
    ecl_12m = exposure * pd_12m * lgd_ecl
    
    sicr = st.checkbox("Augmentation Significative du Risque de Crédit (SICR) ?")
    
    if sicr:
        pd_lifetime = st.slider("PD à maturité (%)", pd_12m*100, 20.0, 5.0) / 100
        ecl_lifetime = exposure * pd_lifetime * lgd_ecl
        provision = ecl_lifetime
        stage = "Étape 2"
        st.warning(f"Actif en {stage} : Provision Lifetime ECL.")
    else:
        provision = ecl_12m
        stage = "Étape 1"
        st.success(f"Actif en {stage} : Provision 12-month ECL.")
        
    st.metric("Provision ECL Requise", f"{provision:.2f} €", delta=f"pour une exposition de {exposure} €")

st.divider()

# --- 3. COMPARAISON AVEC SOLVABILITÉ II ---
st.header("3. IFRS 9 vs. Solvabilité II pour un Assureur")
st.markdown("Bien que les deux visent à mesurer le risque de crédit, leurs philosophies diffèrent.")

data_comp_s2 = {
    "Critère": ["Objectif", "Horizon", "Métrologie", "Impact Bilan"],
    "📉 IFRS 9 (ECL)": [
        "Refléter la perte économique attendue dans le P&L.",
        "12 mois ou Maturité (Lifetime).",
        "**Perte Attendue (Expected Loss)** : PD x LGD x EAD.",
        "Provisionnement direct en déduction de la valeur de l'actif."
    ],
    "🛡️ Solvabilité II (SCR Crédit)": [
        "Calibrer un capital pour couvrir les pertes inattendues.",
        "1 an.",
        "**Perte Inattendue (Unexpected Loss)** : VaR 99.5% sur la distribution des pertes.",
        "Exigence de capital (SCR), n'impacte pas la valeur de l'actif au bilan S2."
    ]
}
st.table(pd.DataFrame(data_comp_s2))

st.info("💡 **Interaction IFRS 9 / IFRS 17 :** Pour les actifs qui backent des passifs d'assurance avec participation, IFRS 9 permet de passer les variations de juste valeur en OCI pour éviter la volatilité dans le P&L (option 'OCI').")