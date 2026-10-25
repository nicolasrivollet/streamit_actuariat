import streamlit as st
import pandas as pd

st.set_page_config(page_title="Architecture Solvabilité II", layout="wide")

st.title("Architecture Réglementaire Solvabilité II")
st.subheader("Comprendre la hiérarchie des normes (Processus Lamfalussy)")

st.markdown("""
La réglementation Solvabilité II n'est pas un bloc monolithique. Elle est structurée en **3 niveaux hiérarchiques**.
Pour un actuaire, savoir si une règle vient de la Directive (Principe) ou du Règlement Délégué (Calcul) est essentiel pour l'interprétation.
""")

st.divider()

# --- 1. LES 3 NIVEAUX ---
st.header("1. La Pyramide Normative")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("### Niveau 1 : Politique\n**Directive 2009/138/CE**")
    st.markdown("""
    *   **Quoi ?** Les principes cadres et les exigences fondamentales.
    *   **Qui ?** Parlement Européen & Conseil.
    *   **Forme :** Doit être transposée dans le droit national (Code des Assurances en France).
    *   *Exemple :* "L'assureur doit détenir un capital suffisant (SCR)."
    """)

with col2:
    st.warning("### Niveau 2 : Technique\n**Règlement Délégué (UE) 2015/35**")
    st.markdown("""
    *   **Quoi ?** Les formules de calcul exactes, les paramètres et les seuils.
    *   **Qui ?** Commission Européenne (sur avis de l'EIOPA).
    *   **Forme :** Application directe (pas de transposition nécessaire).
    *   *Exemple :* "Le choc Actions Type 1 est de 39% + Symmetric Adjustment."
    """)

with col3:
    st.success("### Niveau 3 : Pratique\n**Guidelines EIOPA (ITS / RTS)**")
    st.markdown("""
    *   **Quoi ?** L'interprétation et l'harmonisation des pratiques de supervision.
    *   **Qui ?** EIOPA (Autorité Européenne).
    *   **Forme :** "Comply or Explain" (Appliquer ou expliquer pourquoi on ne le fait pas).
    *   *Exemple :* "Comment traiter les participations stratégiques dans le SCR."
    """)

st.divider()

# --- 2. EXPLORATEUR INTERACTIF ---
st.header("2. Explorateur de Textes par Thématique")
st.markdown("Sélectionnez un sujet pour voir la correspondance entre les textes européens et le Code des Assurances français.")

# Base de connaissances simplifiée
knowledge_base = {
    "Fonds Propres (Own Funds)": {
        "Directive (L1)": "Art. 87 à 99",
        "Règlement Délégué (L2)": "Art. 69 à 82",
        "Code Assurances (FR)": "Art. R351-1 et suivants",
        "Résumé": "Définit la classification en Tiers 1, 2, 3 selon la disponibilité et la subordination."
    },
    "SCR Marché (Standard Formula)": {
        "Directive (L1)": "Art. 105",
        "Règlement Délégué (L2)": "Art. 164 à 181",
        "Code Assurances (FR)": "Art. R352-2",
        "Résumé": "Détaille les chocs : Taux, Actions, Immo, Spread, Change, Concentration."
    },
    "Provisions Techniques (Best Estimate)": {
        "Directive (L1)": "Art. 76 à 86",
        "Règlement Délégué (L2)": "Art. 17 à 42",
        "Code Assurances (FR)": "Art. R351-2",
        "Résumé": "Principes de segmentation, hypothèses, actualisation et Marge de Risque."
    },
    "Gouvernance (Pilier 2)": {
        "Directive (L1)": "Art. 40 à 49",
        "Règlement Délégué (L2)": "Art. 258 à 275",
        "Code Assurances (FR)": "Art. L354-1",
        "Résumé": "Fonctions clés (Actuariat, Risques, Audit, Conformité) et ORSA."
    },
    "Reporting (Pilier 3)": {
        "Directive (L1)": "Art. 35 & 51",
        "Règlement Délégué (L2)": "Art. 290 à 303",
        "Code Assurances (FR)": "Art. L355-1",
        "Résumé": "Contenu du SFCR (Public) et du RSR (Superviseur)."
    }
}

topic = st.selectbox("Choisir une thématique :", list(knowledge_base.keys()))

data = knowledge_base[topic]

col_res1, col_res2 = st.columns([1, 2])

with col_res1:
    st.markdown(f"### 📌 {topic}")
    st.caption(data["Résumé"])

with col_res2:
    df_refs = pd.DataFrame({
        "Référentiel": ["🇪🇺 Directive 2009/138/CE", "🇪🇺 Règlement Délégué 2015/35", "🇫🇷 Code des Assurances"],
        "Articles Clés": [data["Directive (L1)"], data["Règlement Délégué (L2)"], data["Code Assurances (FR)"]]
    })
    st.table(df_refs)

st.info("**Astuce Pro :** En cas de doute, le Règlement Délégué (Niveau 2) prime sur le Code des Assurances pour les calculs techniques, car il est d'application directe.")
