import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Classes d'Actifs & Risques", layout="wide")

st.title("Classes d'Actifs & Cartographie des Risques")
st.subheader("Comprendre le couple Rendement / Risque par typologie d'investissement")

st.markdown("""
Pour un assureur, l'allocation d'actifs est le moteur de la performance financière mais aussi la source principale de consommation de capital (SCR Marché).
Chaque classe d'actif possède un profil de risque spécifique qu'il est crucial de maîtriser pour optimiser le ratio de solvabilité.
""")

st.divider()

# --- 1. ANALYSE PAR CLASSE D'ACTIF ---
st.header("1. Analyse détaillée par Classe d'Actif")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Actions", "Obligations", "Immobilier", "Trésorerie", "Alternatifs"])

with tab1:
    st.subheader("Actions (Equities)")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **Définition :** Titres de propriété d'une entreprise (cotée ou non).
        
        **Profil de Risque :**
        *   **Risque de Marché (Volatilité) :** Le prix peut varier brutalement en fonction de la conjoncture économique.
        *   **Risque de Dividende :** Incertitude sur les flux de revenus futurs.
        """)
    with col2:
        st.info("""
        **Traitement Solvabilité II :**
        *   **Type 1 (OCDE) :** Choc de **39%** + Ajustement Symétrique.
        *   **Type 2 (Autres/Non Coté) :** Choc de **49%** + Ajustement Symétrique.
        *   **Stratégique :** Choc réduit de **22%** (sous conditions).
        """)

with tab2:
    st.subheader("Obligations (Fixed Income)")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **Définition :** Titres de créance émis par des États (Souverain) ou des entreprises (Crédit).
        
        **Profil de Risque :**
        *   **Risque de Taux :** Si les taux montent, la valeur des obligations baisse (Sensibilité/Duration).
        *   **Risque de Crédit (Spread) :** Risque que l'émetteur fasse défaut ou que sa note se dégrade (écartement des spreads).
        """)
    with col2:
        st.info("""
        **Traitement Solvabilité II :**
        *   **Taux :** Choc à la hausse et à la baisse de la courbe.
        *   **Spread :** Choc dépendant de la **Duration** et du **Rating**.
        *   **Souverain (EEE) :** Choc de spread nul (0%) pour les États membres en devise locale.
        """)

with tab3:
    st.subheader("Immobilier (Real Estate)")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **Définition :** Immeubles physiques (Bureaux, Résidentiel, Commerce) ou fonds immobiliers (SCPI, OPCI).
        
        **Profil de Risque :**
        *   **Risque de Liquidité :** Actif difficile à vendre rapidement sans décote importante.
        *   **Risque de Vacance :** Perte de revenus locatifs.
        *   **Risque de Valorisation :** Dépendance aux expertises.
        """)
    with col2:
        st.info("""
        **Traitement Solvabilité II :**
        *   **Choc Standard :** Baisse de **25%** de la valeur de marché.
        """)

with tab4:
    st.subheader("Trésorerie & Monétaire (Cash)")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **Définition :** Dépôts bancaires, comptes à terme, OPCVM monétaires.
        
        **Profil de Risque :**
        *   **Risque d'Inflation :** Érosion du pouvoir d'achat réel si le rendement < inflation.
        *   **Risque de Contrepartie :** Faillite de la banque dépositaire.
        """)
    with col2:
        st.info("""
        **Traitement Solvabilité II :**
        *   **Contrepartie (Type 1) :** Calculé selon la notation de la banque et le montant exposé.
        """)

with tab5:
    st.subheader("Alternatifs (Private Equity, Infra, Hedge Funds)")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **Définition :** Investissements non cotés (Capital Investissement), Dette Privée, Infrastructures.
        
        **Profil de Risque :**
        *   **Illiquidité :** Capital bloqué pour 10 ans ou plus (J-Curve).
        *   **Complexité :** Structures de frais élevées, valorisation "Mark-to-Model".
        """)
    with col2:
        st.info("""
        **Traitement Solvabilité II :**
        *   **Private Equity :** Généralement choc Actions Type 2 (**49%**).
        *   **Infrastructure (Qualifiée) :** Choc réduit (**30%**).
        """)

st.divider()

# --- 2. MATRICE DES RISQUES ---
st.header("2. Matrice Synthétique des Risques")
st.markdown("Intensité du risque : 🟢 Faible | 🟡 Moyen | 🔴 Élevé")

data = {
    "Classe d'Actif": ["Actions", "Oblig. Souveraines", "Oblig. Crédit (IG)", "Immobilier", "Cash", "Private Equity"],
    "Marché (Volatilité)": ["🔴", "🟡", "🟡", "🟡", "🟢", "🔴"],
    "Taux d'Intérêt": ["🟢", "🔴", "🔴", "🟡", "🟢", "🟢"],
    "Crédit (Défaut)": ["N/A", "🟢", "🟡", "N/A", "🟡", "🔴"],
    "Liquidité": ["🟢", "🟢", "🟡", "🔴", "🟢", "🔴"],
    "Inflation": ["🟡", "🔴", "🔴", "🟢", "🔴", "🟢"]
}

df = pd.DataFrame(data)
st.table(df)

st.caption("IG : Investment Grade (Noté BBB- ou plus).")

st.divider()

# --- 3. VISUALISATION RENDEMENT / RISQUE ---
st.header("3. Cartographie Rendement / Risque (Efficient Frontier)")
st.markdown("Positionnement relatif des classes d'actifs (Données de marché illustratives).")

# Données pour le graphique
data_viz = {
    "Classe d'Actif": ["Cash", "Oblig. Gouv (Core)", "Oblig. Crédit (IG)", "Immobilier", "Actions (Monde)", "Private Equity", "Hedge Funds"],
    "Rendement Espéré (%)": [3.0, 3.5, 4.5, 5.5, 7.5, 9.0, 6.0],
    "Volatilité (%)": [0.5, 4.0, 6.0, 12.0, 18.0, 25.0, 10.0],
    "Type": ["Monétaire", "Taux", "Crédit", "Réel", "Action", "Action", "Alternatif"]
}
df_viz = pd.DataFrame(data_viz)

fig = px.scatter(df_viz, x="Volatilité (%)", y="Rendement Espéré (%)", color="Type", text="Classe d'Actif", size=[20]*7,
                 title="Couple Rendement / Risque", template="plotly_white")
fig.update_traces(textposition='top center')
fig.update_layout(xaxis_title="Risque (Volatilité)", yaxis_title="Rendement Attendu")

st.plotly_chart(fig, use_container_width=True)

# --- 4. IMPACT CAPITAL (SCR) ---
st.header("4. Consommation de Capital (SCR Marché)")
st.markdown("Comparaison des chocs réglementaires (Formule Standard) par classe d'actif.")

data_scr = {
    "Classe d'Actif": ["Cash", "Oblig. Gouv (EEE)", "Immobilier", "Infra (Qualif.)", "Actions (Type 1)", "Actions (Type 2)", "Private Equity"],
    "Choc S2 (%)": [0, 0, 25, 30, 39, 49, 49]
}
df_scr = pd.DataFrame(data_scr)
fig_scr = px.bar(df_scr, x="Classe d'Actif", y="Choc S2 (%)", color="Choc S2 (%)", title="Intensité du Choc en Capital", color_continuous_scale="Reds")
st.plotly_chart(fig_scr, use_container_width=True)

# --- 5. CONTEXTE STRATÉGIQUE (ALM) ---
st.header("5. La Stratégie d'Investissement (ALM)")
st.markdown("""
L'allocation d'actifs d'un assureur n'est pas libre. Elle est contrainte par le passif (les engagements envers les assurés).
C'est le principe du **Liability Driven Investment (LDI)**.
""")

col_alm1, col_alm2 = st.columns(2)

with col_alm1:
    st.subheader("Contraintes de Passif")
    st.write("""
    *   **Duration :** L'actif doit avoir une sensibilité aux taux proche du passif pour immuniser le bilan.
    *   **Liquidité :** Il faut assez de cash pour payer les sinistres (rachats, décès).
    *   **Devise :** Congruence (Matching) des devises Actif/Passif pour éviter le risque de change.
    """)

with col_alm2:
    st.subheader("Contraintes Réglementaires")
    st.write("""
    *   **Principe de la Personne Prudente (PPP) :** N'investir que dans ce que l'on comprend et maîtrise.
    *   **Diversification :** Éviter la concentration sur un seul émetteur.
    *   **SCR :** L'allocation doit tenir compte du coût en capital (un actif à haut rendement peut détruire de la valeur si son coût en SCR est trop élevé).
    """)