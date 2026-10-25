import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- LOGIQUE DE CALCUL RÉGLEMENTAIRE (Moteur Solvabilité II) ---

def calculate_diversified_scr(scr_dict):
    """
    Applique la matrice de corrélation EIOPA pour le SCR Marché.
    Ordre standard : Equity, Spread, Property.
    """
    risk_map = {"Equity": 0, "Spread": 1, "Property": 2}
    scr_vector = np.zeros(3)
    
    for risk, value in scr_dict.items():
        if risk in risk_map:
            scr_vector[risk_map[risk]] = value
            
    # Matrice de corrélation simplifiée du Règlement Délégué (UE) 2015/35
    corr_matrix = np.array([
        [1.00, 0.75, 0.75], # Equity
        [0.75, 1.00, 0.50], # Spread
        [0.75, 0.50, 1.00]  # Property
    ])
    
    # Formule matricielle : sqrt(SCR^T * Corr * SCR)
    scr_total = np.sqrt(np.dot(scr_vector.T, np.dot(corr_matrix, scr_vector)))
    return scr_total

# --- INTERFACE UTILISATEUR STREAMLIT ---

st.title("SCR Asset Screener & Analyse de Rentabilité")
st.markdown("""
Cet outil simule l'impact d'un nouvel investissement sur le **Capital de Solvabilité Requis (SCR)** du GACM. 
Il permet d'évaluer l'efficacité de l'investissement en termes de consommation de capital et son impact sur le ratio de solvabilité.
""")

st.divider()

# --- SECTION 1 : SAISIE DES CARACTÉRISTIQUES ---
st.header("1⃣ Caractéristiques de l'Investissement")
col_a, col_b = st.columns(2)

with col_a:
    asset_type = st.selectbox("Classe d'actif (Module SCR)", ["Obligations", "Actions", "Immobilier"])
    nominal = st.number_input("Montant investi (€)", min_value=0, value=1000000, step=100000)

with col_b:
    yield_expected = st.number_input("Rendement annuel attendu (%)", value=4.50, step=0.05) / 100
    if asset_type == "Obligations":
        rating = st.select_slider("Notation (Rating)", options=["AAA", "AA", "A", "BBB", "HY"], value="BBB")
        duration = st.slider("Sensibilité & Horizon (Années)", 1.0, 20.0, 6.0)
        horizon = duration
    else:
        rating, duration = None, 0
        horizon = st.slider("Horizon de détention (Années)", 1, 20, 5)

st.divider()

# --- SECTION 2 : CALCUL DU SCR MARGINAL ---
st.header("2⃣ Évaluation du Risque (Formule Standard)")

scr_results = {}
st.markdown("### Détail des chocs réglementaires")

col_text, col_calc = st.columns([2, 1])

with col_text:
    if asset_type == "Actions":
        st.info("**Module Action :** Application d'un choc de **39%** (Type 1 - Marchés développés) selon l'Article 169 du Règlement Délégué.")
        scr_results["Equity"] = nominal * 0.39
    
    elif asset_type == "Obligations":
        # Facteurs de stress Spread EIOPA (simplifiés pour démonstration)
        stress_map = {"AAA": 0.009, "AA": 0.011, "A": 0.014, "BBB": 0.025, "HY": 0.045}
        f_spread = stress_map[rating]
        st.info(f"**Module Spread :** Application d'un choc basé sur le rating (**{rating}**) et la duration (**{duration:.1f}**).")
        st.latex(r"SCR_{Spread} = Nominal \times Duration \times F(Rating)")
        scr_results["Spread"] = nominal * duration * f_spread
        
    elif asset_type == "Immobilier":
        st.info("**Module Immobilier :** Application d'un choc forfaitaire de **25%** (Article 174).")
        scr_results["Property"] = nominal * 0.25

with col_calc:
    for risk, val in scr_results.items():
        st.metric(f"SCR {risk}", f"{val:,.0f} €")

# Calcul de la diversification
scr_div = calculate_diversified_scr(scr_results)
diversification_gain = sum(scr_results.values()) - scr_div

# --- SECTION 3 : EFFICACITÉ DU CAPITAL (Vision Horizon) ---
st.divider()
st.header("3⃣ Efficacité du Capital (Vision Horizon)")

# Analyse : Génération Totale vs Consommation de Capital
# On regarde si l'investissement génère plus de FP sur sa durée de vie qu'il n'en consomme en SCR instantané.
generation_fp_total = nominal * yield_expected * horizon
ratio_recouvrement = generation_fp_total / scr_div if scr_div > 0 else 0

# Affichage des métriques clés
m1, m2, m3 = st.columns(3)
m1.metric("SCR Consommé", f"{scr_div:,.0f} €", delta="Exigence de Capital", delta_color="inverse")
m2.metric(f"Génération FP ({horizon} ans)", f"{generation_fp_total:,.0f} €", help="Cumul des revenus financiers attendus sur l'horizon.")
m3.metric("Ratio Recouvrement SCR", f"{ratio_recouvrement:.1%}", delta="Génération / SCR")

# --- VISUALISATION ---
col_plot, col_analysis = st.columns([1.5, 1])

with col_plot:
    # Jauge de Recouvrement
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = ratio_recouvrement * 100,
        title = {'text': "Couverture du SCR par les revenus (%)", 'font': {'size': 16}},
        gauge = {
            'axis': {'range': [0, 200]}, # Echelle adaptée (0-200%)
            'bar': {'color': "#1E88E5"},
            'steps': [
                {'range': [0, 100], 'color': "#FFCDD2"}, # < 100% (Ne couvre pas le SCR)
                {'range': [100, 200], 'color': "#C8E6C9"}], # > 100% (Couvre le SCR)
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 100}})) # Seuil 100%
    fig_gauge.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig_gauge, use_container_width=True)

with col_analysis:
    st.subheader("Analyse Stratégique")
    
    # Calculs complémentaires pour l'aide à la décision
    revenu_annuel = nominal * yield_expected
    payback = scr_div / revenu_annuel if revenu_annuel > 0 else 999
    breakeven_yield = scr_div / (nominal * horizon) if (nominal * horizon) > 0 else 0
    
    st.write(f"""
    Sur un horizon de **{horizon} ans**, cet investissement génère **{generation_fp_total:,.0f} €** de revenus cumulés.
    
    Comparé au SCR initial de **{scr_div:,.0f} €**, le ratio de recouvrement est de **{ratio_recouvrement*100:.1f}%**.
    """)
    
    st.markdown(f"""
    **Indicateurs de décision :**
    *   ⏳ **Payback SCR :** **{payback:.1f} ans** pour amortir le coût en capital.
    *   **Yield Breakeven :** Il faudrait un rendement min. de **{breakeven_yield*100:.2f}%** pour être à l'équilibre sur la période.
    """)
    
    if ratio_recouvrement > 1.0:
        st.success("**AUTO-FINANCEMENT : OUI**")
        st.write("Les revenus cumulés couvrent l'exigence de capital.")
    else:
        st.error("**AUTO-FINANCEMENT : NON**")
        st.write("L'actif consomme plus de capital qu'il ne rapporte.")


# --- DÉTAILS TECHNIQUES ---
with st.expander("📚 Rappels Réglementaires (S2)", expanded=True):
    st.markdown(r"""
    **Ratio de Recouvrement du SCR :**
    Cet indicateur compare la somme des revenus financiers générés sur l'horizon de détention au montant de capital bloqué (SCR).
    
    $$ \text{Ratio} = \frac{\sum \text{Revenus Financiers}}{\text{SCR Initial}} $$
    
    Si le ratio est > 100%, l'actif génère suffisamment de cash pour "rembourser" virtuellement l'exigence de capital qu'il a créée.
    
    **La Matrice de Corrélation :** Elle permet de calculer le SCR Diversifié en tenant compte de la faible probabilité 
    que tous les chocs de marché (Action, Spread, Immo) atteignent leur intensité maximale simultanément.
    """)
    corr_df = pd.DataFrame(
        [[1.00, 0.75, 0.75], [0.75, 1.00, 0.50], [0.75, 0.50, 1.00]],
        index=["Equity", "Spread", "Property"],
        columns=["Equity", "Spread", "Property"]
    )
    st.table(corr_df)