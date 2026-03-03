import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Réglementation Bâle III", layout="wide")

st.title("🏦 Bâle III : La Réglementation Prudentielle Bancaire")
st.subheader("Renforcer la résilience du système bancaire mondial")

st.markdown("""
Suite à la crise financière de 2008, le **Comité de Bâle sur le Contrôle Bancaire (BCBS)** a publié un ensemble de réformes, connues sous le nom de **Bâle III**, pour renforcer la réglementation, la surveillance et la gestion des risques du secteur bancaire.

L'objectif est double :
1.  **Améliorer la qualité et la quantité du capital** pour mieux absorber les chocs.
2.  **Introduire de nouvelles exigences en matière de liquidité**.
""")

st.divider()

# --- 1. LES 3 PILIERS ---
st.header("1. L'Architecture en 3 Piliers")
st.markdown("Comme Solvabilité II, Bâle III est structuré en trois piliers complémentaires.")

tab1, tab2, tab3 = st.tabs(["📊 Pilier 1 : Exigences Minimales", "⚖️ Pilier 2 : Surveillance Prudentielle", "📢 Pilier 3 : Discipline de Marché"])

with tab1:
    st.subheader("Pilier 1 : Exigences Quantitatives")
    st.markdown("Ce pilier fixe les ratios minimaux de capital et de liquidité.")
    
    st.info("#### Ratios de Capital")
    st.markdown(r"""
    Le capital est mesuré en pourcentage des **Actifs Pondérés par le Risque (RWA - Risk-Weighted Assets)**.
    *   **Ratio CET1 (Common Equity Tier 1) :** Le capital "dur" (actions ordinaires, bénéfices non distribués). Seuil min : **4.5%**.
    *   **Ratio Tier 1 :** CET1 + Autres instruments Tier 1 (ex: obligations hybrides). Seuil min : **6.0%**.
    *   **Ratio Total :** Tier 1 + Capital Tier 2 (dette subordonnée). Seuil min : **8.0%**.
    
    À cela s'ajoutent des **coussins de capital** (Conservation, Contracyclique, Systémique) portant l'exigence totale bien au-delà de 8%.
    """)
    
    st.warning("#### Nouveaux Ratios de Liquidité")
    st.markdown("""
    *   **LCR (Liquidity Coverage Ratio) :** Vise à assurer la survie à court terme (30 jours) en cas de crise de liquidité.
        $$ LCR = \frac{\text{Stock d'actifs liquides de haute qualité (HQLA)}}{\text{Sorties de trésorerie nettes sur 30 jours}} \ge 100\% $$
    *   **NSFR (Net Stable Funding Ratio) :** Vise à assurer la stabilité du financement à long terme (1 an).
        $$ NSFR = \frac{\text{Financement stable disponible}}{\text{Financement stable requis}} \ge 100\% $$
    """)
    
    st.error("#### Ratio de Levier (Leverage Ratio)")
    st.markdown("Un filet de sécurité non basé sur les risques. Il mesure le capital Tier 1 par rapport à l'exposition totale (non pondérée). Seuil min : **3%**.")

with tab2:
    st.subheader("Pilier 2 : Processus de Surveillance Prudentielle")
    st.markdown("""
    Ce pilier vise à s'assurer que les banques ont des processus internes robustes pour évaluer leurs risques et leur adéquation en capital, et que les superviseurs peuvent intervenir.
    
    *   **ICAAP (Internal Capital Adequacy Assessment Process) :** L'équivalent de l'**ORSA** pour les banques. La banque doit évaluer elle-même ses besoins en capital, au-delà des exigences du Pilier 1.
    *   **SREP (Supervisory Review and Evaluation Process) :** Le processus par lequel le superviseur (BCE/ACPR) évalue l'ICAAP de la banque et peut imposer des exigences de capital supplémentaires (le "Pillar 2 Requirement").
    """)

with tab3:
    st.subheader("Pilier 3 : Discipline de Marché")
    st.markdown("""
    Ce pilier vise à renforcer la transparence en imposant la publication d'informations détaillées sur le profil de risque, l'adéquation des fonds propres et les processus de gestion des risques de la banque.
    Cela permet aux marchés, aux analystes et aux contreparties de mieux évaluer la solidité de l'institution.
    """)

st.divider()

# --- 2. BÂLE IV / FINALISATION ---
st.header("2. La Finalisation de Bâle III (surnommée 'Bâle IV')")
st.markdown("""
Pour restaurer la crédibilité et la comparabilité des ratios, les réformes finales de Bâle III (applicables à partir de 2025) introduisent une mesure phare : l'**Output Floor**.
""")

st.success("""
### Plancher de Capital (Output Floor)
Les banques utilisant des modèles internes (IRB) pour calculer leurs RWA ne pourront plus obtenir un avantage en capital illimité.

$$ \text{RWA}_{\text{Total}} \ge 72.5\% \times \text{RWA}_{\text{Approche Standard}} $$

**Conséquence :** Le capital calculé par les modèles internes ne pourra jamais être inférieur à 72.5% de ce qu'il serait en utilisant l'approche standard, moins sensible aux risques.
""")

st.divider()

# --- 3. COMPARAISON BÂLE III vs SOLVABILITÉ II ---
st.header("3. Comparaison avec Solvabilité II")
st.markdown("Bien que les philosophies soient proches (approche par les risques, 3 piliers), des différences majeures existent.")

data_comp = {
    "Critère": ["Objectif Principal", "Métrologie du Risque", "Vision du Bilan", "Ratio de Liquidité (Pilier 1)"],
    "🏦 Bâle III (Banque)": [
        "Stabilité financière, éviter le risque systémique.",
        "**RWA (Risk-Weighted Assets)** : Pondération des actifs selon leur risque de crédit/marché.",
        "Bilan comptable ajusté.",
        "**Oui (LCR & NSFR)** : Exigences explicites et quantifiées."
    ],
    "🛡️ Solvabilité II (Assurance)": [
        "Protection des assurés, continuité des paiements.",
        "**SCR (Solvency Capital Requirement)** : Calcul de la perte à 1 an (VaR 99.5%) sur l'ensemble du bilan (Actif & Passif).",
        "Bilan économique (Market Consistent).",
        "**Non** : La liquidité est un risque qualitatif géré sous le Pilier 2 (ORSA)."
    ]
}
df_comp = pd.DataFrame(data_comp)
st.table(df_comp)

st.info("💡 **Point Clé :** La principale différence réside dans la nature du passif. Une banque a un passif exigible à court terme (dépôts), d'où l'importance du LCR. Un assureur a un passif long et prévisible (rentes, sinistres), d'où l'importance de l'actualisation et de l'ALM.")