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
    st.markdown("**LCR (Liquidity Coverage Ratio) :** Vise à assurer la survie à court terme (30 jours) en cas de crise de liquidité.")
    st.latex(r"LCR = \frac{\text{Stock d'actifs liquides de haute qualité (HQLA)}}{\text{Sorties de trésorerie nettes sur 30 jours}} \ge 100\%")
    
    st.markdown("**NSFR (Net Stable Funding Ratio) :** Vise à assurer la stabilité du financement à long terme (1 an).")
    st.latex(r"NSFR = \frac{\text{Financement stable disponible}}{\text{Financement stable requis}} \ge 100\%")
    
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

# --- CALCULATEUR DE RATIOS ---
st.header("Calculateur de Ratios de Capital")
st.markdown("Simulez l'impact de la structure du bilan sur les ratios prudentiels.")

col_bilan1, col_bilan2 = st.columns(2)

with col_bilan1:
    st.subheader("Structure des Actifs (RWA)")
    credit_corporate = st.slider("Exposition Crédit Corporate (M€)", 1000, 10000, 5000)
    credit_retail = st.slider("Exposition Crédit Retail (M€)", 1000, 10000, 3000)
    credit_souverain = st.slider("Exposition Souveraine (M€)", 1000, 10000, 2000)
    
    # Pondérations de risque (Approche Standard simplifiée)
    rwa = credit_corporate * 1.0 + credit_retail * 0.75 + credit_souverain * 0.0
    
    st.metric("Total Actifs Pondérés (RWA)", f"{rwa/1000:.1f} Md€")

with col_bilan2:
    st.subheader("Structure du Capital")
    cet1_capital = st.slider("Capital CET1 (M€)", 100, 1000, 400)
    at1_capital = st.slider("Capital AT1 (M€)", 0, 500, 100)
    t2_capital = st.slider("Capital Tier 2 (M€)", 0, 500, 150)
    
    total_capital = cet1_capital + at1_capital + t2_capital
    st.metric("Total Capital Prudentiel", f"{total_capital} M€")

# Calcul des ratios
cet1_ratio = cet1_capital / rwa if rwa > 0 else 0
t1_ratio = (cet1_capital + at1_capital) / rwa if rwa > 0 else 0
total_ratio = total_capital / rwa if rwa > 0 else 0

st.subheader("Ratios de Solvabilité Calculés")
c_res1, c_res2, c_res3 = st.columns(3)
c_res1.metric("Ratio CET1", f"{cet1_ratio:.1%}", delta="Min: 4.5%", delta_color="normal" if cet1_ratio >= 0.045 else "inverse")
c_res2.metric("Ratio Tier 1", f"{t1_ratio:.1%}", delta="Min: 6.0%", delta_color="normal" if t1_ratio >= 0.06 else "inverse")
c_res3.metric("Ratio Total", f"{total_ratio:.1%}", delta="Min: 8.0%", delta_color="normal" if total_ratio >= 0.08 else "inverse")

# --- 2. BÂLE IV / FINALISATION ---
st.header("2. La Finalisation de Bâle III (surnommée 'Bâle IV')")
st.markdown("""
Pour restaurer la crédibilité et la comparabilité des ratios, les réformes finales de Bâle III (applicables à partir de 2025 en Europe via CRR3) introduisent des changements structurels majeurs au-delà du simple Output Floor.
""")

col_b4_1, col_b4_2 = st.columns(2)

with col_b4_1:
    st.success(r"""
    ### 🛡️ Output Floor (Plancher)
    Les banques utilisant des modèles internes ne pourront plus bénéficier d'un allègement de capital illimité.
    
    $$ \text{RWA}_{\text{Interne}} \ge 72.5\% \times \text{RWA}_{\text{Standard}} $$
    
    **Objectif :** Limiter l'optimisation des modèles.
    """)
    
    st.warning("""
    ### 📉 Risque de Marché (FRTB)
    **Fundamental Review of the Trading Book**
    *   Passage de la VaR à l'**Expected Shortfall (ES)** pour les modèles internes (meilleure capture des risques extrêmes).
    *   Frontière plus stricte entre Trading Book et Banking Book.
    """)

with col_b4_2:
    st.info("""
    ### 🛠️ Risque Opérationnel
    **Suppression des modèles internes (AMA).**
    Remplacement par une approche standard unique (SMA) basée sur :
    1.  La taille de la banque (Business Indicator).
    2.  L'historique des pertes opérationnelles.
    """)
    
    st.error("""
    ### ⚠️ CVA (Credit Valuation Adj.)
    Révision du cadre pour le risque de contrepartie sur dérivés.
    Suppression de l'approche interne pour la CVA, remplacée par des approches standardisées.
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