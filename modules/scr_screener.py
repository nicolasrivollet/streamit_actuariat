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

st.title("🛡️ SCR Asset Screener & Analyse de Rentabilité")
st.markdown("""
Cet outil simule l'impact d'un nouvel investissement sur le **Capital de Solvabilité Requis (SCR)** du GACM. 
Il permet d'évaluer l'efficacité de l'investissement en termes de consommation de capital et son impact sur le ratio de solvabilité.
""")

st.divider()

# --- SECTION 1 : SAISIE DES CARACTÉRISTIQUES ---
st.header("1️⃣ Caractéristiques de l'Investissement")
col_a, col_b = st.columns(2)

with col_a:
    asset_type = st.selectbox("Classe d'actif (Module SCR)", ["Obligations", "Actions", "Immobilier"])
    nominal = st.number_input("Montant investi (€)", min_value=0, value=1000000, step=100000)

with col_b:
    yield_expected = st.number_input("Rendement annuel attendu (%)", value=4.50, step=0.05) / 100
    if asset_type == "Obligations":
        rating = st.select_slider("Notation (Rating)", options=["AAA", "AA", "A", "BBB", "HY"], value="BBB")
        duration = st.slider("Sensibilité (Duration modifiée)", 0.0, 20.0, 6.0)
    else:
        rating, duration = None, 0

st.divider()

# --- SECTION 2 : CALCUL DU SCR MARGINAL ---
st.header("2️⃣ Évaluation du Risque (Formule Standard)")

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

# --- SECTION 3 : EFFICACITÉ DU CAPITAL (RoSCR) ---
st.divider()
st.header("3️⃣ Efficacité du Capital (Rentabilité sur SCR)")

# Analyse : Rentabilité vs Consommation de Capital
# La "Génération de Fonds Propres" est le résultat financier attendu (net de l'investissement initial).
generation_fp = nominal * yield_expected
roscr = generation_fp / scr_div if scr_div > 0 else 0

# Affichage des métriques clés
m1, m2, m3 = st.columns(3)
m1.metric("SCR Consommé", f"{scr_div:,.0f} €", delta="Exigence de Capital", delta_color="inverse")
m2.metric("Génération FP (1 an)", f"{generation_fp:,.0f} €", help="Revenus financiers attendus (Rendement)")
m3.metric("Rentabilité sur SCR (RoSCR)", f"{roscr:.1%}", delta="Rendement / SCR")

# --- VISUALISATION ---
col_plot, col_analysis = st.columns([1.5, 1])

with col_plot:
    # Jauge de RoSCR
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = roscr * 100,
        title = {'text': "RoSCR (%)", 'font': {'size': 16}},
        gauge = {
            'axis': {'range': [0, 30]}, # Echelle adaptée au RoSCR (ex: 0-30%)
            'bar': {'color': "#1E88E5"},
            'steps': [
                {'range': [0, 5], 'color': "#FFCDD2"}, # < 5% (Faible)
                {'range': [5, 10], 'color': "#FFF9C4"}, # 5-10% (Moyen)
                {'range': [10, 30], 'color': "#C8E6C9"}], # > 10% (Bon)
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 10}})) # Seuil indicatif 10%
    fig_gauge.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig_gauge, use_container_width=True)

with col_analysis:
    st.subheader("Analyse Stratégique")
    st.write(f"""
    Pour chaque euro de capital réglementaire immobilisé (**SCR**), cet investissement génère **{roscr*100:.1f} centimes** de résultat financier annuel.
    """)
    
    if roscr > 0.10:
        st.success("**EFFICACITÉ : ÉLEVÉE**")
        st.write("L'actif rémunère très bien le capital consommé (> 10%).")
    elif roscr > 0.05:
        st.warning("**EFFICACITÉ : MOYENNE**")
        st.write("La rentabilité couvre le coût du capital mais sans marge excessive.")
    else:
        st.error("**EFFICACITÉ : FAIBLE**")
        st.write("La consommation de SCR est trop élevée par rapport au rendement offert.")

# --- SECTION 4 : RENTABILITÉ ÉCONOMIQUE ---
st.divider()
st.header("4️⃣ Rentabilité Économique (Génération Nette)")
st.markdown("Évaluation de la création de valeur après rémunération du capital immobilisé.")

col_rent1, col_rent2 = st.columns(2)

with col_rent1:
    coc_rate = st.slider("Taux de rémunération cible des FP (%)", 0.0, 20.0, 10.0, 0.5, help="Objectif de rentabilité sur le capital alloué (ROE Cible).") / 100
    
    revenu_annuel = nominal * yield_expected
    cout_scr = scr_div * coc_rate
    generation_nette = revenu_annuel - cout_scr
    
    st.metric("Revenus Financiers (1 an)", f"{revenu_annuel:,.0f} €", delta=f"Yield {yield_expected*100:.2f}%")
    st.metric("Génération Nette de FP", f"{generation_nette:,.0f} €", delta_color="normal" if generation_nette > 0 else "inverse")

with col_rent2:
    fig_water = go.Figure(go.Waterfall(
        orientation = "v",
        measure = ["relative", "relative", "total"],
        x = ["Revenus Financiers", "Charge Capital", "Génération Nette"],
        textposition = "outside",
        text = [f"+{revenu_annuel:,.0f}", f"-{cout_scr:,.0f}", f"{generation_nette:,.0f}"],
        y = [revenu_annuel, -cout_scr, generation_nette],
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
    ))
    fig_water.update_layout(title="Création de Valeur (1 an)", height=300)
    st.plotly_chart(fig_water, use_container_width=True)

# --- DÉTAILS TECHNIQUES ---
with st.expander("📚 Rappels Réglementaires (S2)"):
    st.markdown(r"""
    **Return on Solvency Capital Requirement (RoSCR) :**
    Indicateur clé pour l'allocation d'actifs sous contrainte Solvabilité II.
    
    $$ \text{RoSCR} = \frac{\text{Rendement Espéré (€)}}{\text{SCR Marginal (€)}} $$
    
    Il permet de comparer des actifs hétérogènes (ex: Obligations vs Actions) sur une base commune : la rémunération du risque réglementaire.
    
    **La Matrice de Corrélation :** Elle permet de calculer le SCR Diversifié en tenant compte de la faible probabilité 
    que tous les chocs de marché (Action, Spread, Immo) atteignent leur intensité maximale simultanément.
    """)
    corr_df = pd.DataFrame(
        [[1.00, 0.75, 0.75], [0.75, 1.00, 0.50], [0.75, 0.50, 1.00]],
        index=["Equity", "Spread", "Property"],
        columns=["Equity", "Spread", "Property"]
    )
    st.table(corr_df)