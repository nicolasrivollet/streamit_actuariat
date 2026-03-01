import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Qualité des Données S2", layout="wide")

st.title("🗃️ Qualité des Données (Data Quality) - Solvabilité II")
st.subheader("Le carburant du moteur Solvabilité II")

st.markdown("""
Dans Solvabilité II, la qualité des données n'est pas une option, c'est une exigence réglementaire stricte (Article 82 de la Directive).
Des données de mauvaise qualité entraînent un mauvais calcul des Provisions Techniques (Best Estimate), du SCR, une mauvaise gestion des risques et in fine, des sanctions du superviseur.
""")

st.divider()

# --- 1. LES CRITÈRES ACA ---
st.header("1. Les 3 Critères d'Or (ACA)")
st.markdown("Pour être utilisables dans le calcul des provisions techniques et du SCR, les données doivent respecter trois critères cumulatifs :")

c1, c2, c3 = st.columns(3)

with c1:
    st.info("### ✅ Exactitude (Accuracy)")
    st.write("""
    La donnée doit refléter la réalité sans erreur.
    *   *Exemple :* La date de naissance de l'assuré est correcte.
    *   *Contrôle :* Comparaison avec pièces justificatives, cohérence date naissance vs date adhésion.
    """)

with c2:
    st.warning("### 📚 Exhaustivité (Completeness)")
    st.write("""
    Toutes les données nécessaires sont présentes. Pas de trous.
    *   *Exemple :* Tous les sinistres survenus sont enregistrés.
    *   *Contrôle :* Rapprochement Comptabilité vs Gestion (Inventaire).
    """)

with c3:
    st.success("### 🎯 Pertinence (Appropriateness)")
    st.write("""
    La donnée est adaptée au modèle utilisé.
    *   *Exemple :* Utiliser une table de mortalité "Cadres" pour une population "Ouvriers" n'est pas approprié.
    *   *Contrôle :* Backtesting, analyse de représentativité.
    """)

st.divider()

# --- 2. GOUVERNANCE DES DONNÉES ---
st.header("2. Gouvernance & Documentation")
st.markdown("L'assureur doit formaliser sa gestion des données à travers plusieurs documents clés.")

tab1, tab2, tab3 = st.tabs(["Politique de Qualité", "Dictionnaire des Données", "Répertoire des Données"])

with tab1:
    st.markdown("**La Politique de Qualité des Données :** Document validé par le Conseil d'Administration qui définit les rôles (Data Owner, Data Steward), les objectifs de qualité et les processus de remédiation.")
with tab2:
    st.markdown("**Le Dictionnaire des Données :** La 'Bible' technique. Pour chaque champ (ex: `POL_ID`), il définit le format (String, Int), la source, et la signification métier.")
with tab3:
    st.markdown("**Le Répertoire des Données (Data Directory) :** Cartographie des flux. D'où vient la donnée ? Par quelles applications passe-t-elle ? Où est-elle stockée ? C'est essentiel pour la traçabilité (Audit Trail).")

st.divider()

# --- 3. OUTIL D'AUTO-ÉVALUATION ---
st.header("3. Scorecard Qualité des Données")
st.write("Évaluez la maturité de votre dispositif Data Quality :")

col_q1, col_q2 = st.columns(2)
with col_q1:
    q1 = st.select_slider("Documentation des données (Dictionnaire à jour ?)", options=["Inexistant", "Partiel", "Complet", "Auditée"], value="Partiel")
    q2 = st.select_slider("Contrôles automatisés (Bloquants ?)", options=["Aucun", "Manuels", "Automatiques", "Temps réel"], value="Manuels")
with col_q2:
    q3 = st.select_slider("Rapprochement Compta-Gestion", options=["Annuel", "Trimestriel", "Mensuel", "Automatisé"], value="Trimestriel")
    q4 = st.select_slider("Gouvernance (Data Owners nommés ?)", options=["Non", "Informel", "Officiel", "Actif"], value="Informel")

# Calcul score simple
score_map = {"Inexistant": 0, "Aucun": 0, "Non": 0, "Annuel": 1,
             "Partiel": 1, "Manuels": 1, "Informel": 1, "Trimestriel": 2,
             "Complet": 2, "Automatiques": 2, "Officiel": 2, "Mensuel": 3,
             "Auditée": 3, "Temps réel": 3, "Actif": 3, "Automatisé": 4}

total_score = score_map[q1] + score_map[q2] + score_map[q3] + score_map[q4]
max_score = 13 # 3+3+3+4 approx

col_score, col_chart = st.columns([1, 2])

with col_score:
    st.metric("Score Maturité Data", f"{total_score}/{max_score}")
    if total_score < 5:
        st.error("Niveau : Insuffisant (Risque de majoration SCR)")
    elif total_score < 9:
        st.warning("Niveau : En progrès")
    else:
        st.success("Niveau : Robuste")

with col_chart:
    # Radar chart
    df_radar = pd.DataFrame(dict(
        r=[score_map[q1], score_map[q2], score_map[q3], score_map[q4]],
        theta=['Documentation', 'Contrôles', 'Rapprochement', 'Gouvernance']
    ))
    fig = px.line_polar(df_radar, r='r', theta='theta', line_close=True, range_r=[0, 4])
    fig.update_traces(fill='toself')
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.caption("Référence : Article 82 de la Directive Solvabilité II & Guidelines EIOPA sur la qualité des données.")