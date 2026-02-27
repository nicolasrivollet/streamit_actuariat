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
Il permet de confronter le rendement attendu au coût réglementaire du capital (6%) pour évaluer la création de valeur économique.
""")

st.divider()

# --- SECTION 1 : SAISIE DES CARACTÉRISTIQUES ---
st.header("1️⃣ Caractéristiques de l'Investissement")
col_a, col_b = st.columns(2)

with col_a:
    asset_name = st.text_input("Nom de l'actif / Émetteur", "Obligation Corporate BBB+")
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

# --- SECTION 3 : RENTABILITÉ ET GÉNÉRATION DE FONDS PROPRES ---
st.divider()
st.header("3️⃣ Indicateurs de Rentabilité et Solvabilité")

# Paramètres économiques
k_cost_rate = 0.06  # Coût du capital réglementaire (Risk Margin CoC)
revenu_annuel = nominal * yield_expected
cout_immobilisation = scr_div * k_cost_rate
generation_nette = revenu_annuel - cout_immobilisation
raroc = revenu_annuel / scr_div if scr_div > 0 else 0

# Affichage des métriques clés
m1, m2, m3 = st.columns(3)
m1.metric("SCR Diversifié", f"{scr_div:,.0f} €")
m2.metric("Génération Nette de FP", f"{generation_nette:,.0f} €", delta=f"{raroc:.2%} vs 6%")
m3.metric("RAROC", f"{raroc:.2%}")

# --- VISUALISATION ---
col_plot, col_analysis = st.columns([1.5, 1])

with col_plot:
    # Jauge de rentabilité
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = raroc * 100,
        title = {'text': "RAROC (%) vs Coût du Capital (6%)", 'font': {'size': 16}},
        gauge = {
            'axis': {'range': [None, 15]},
            'bar': {'color': "#1E88E5"},
            'steps': [
                {'range': [0, 6], 'color': "#FFCDD2"},
                {'range': [6, 15], 'color': "#C8E6C9"}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 6}}))
    fig_gauge.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig_gauge, use_container_width=True)

with col_analysis:
    st.subheader("Analyse Stratégique")
    st.write(f"""
    L'actif dégage un revenu brut de **{revenu_annuel:,.0f} €**. 
    Cependant, l'immobilisation de **{scr_div:,.0f} €** de fonds propres engendre un coût d'opportunité 
    théorique de **{cout_immobilisation:,.0f} €** (au taux de 6%).
    """)
    
    if raroc > k_cost_rate:
        st.success("**AVIS RISQUE : FAVORABLE**")
        st.write("L'investissement auto-finance sa consommation de capital et génère un surplus de solvabilité.")
    else:
        st.warning("**AVIS RISQUE : RÉSERVÉ**")
        st.write("La rentabilité est insuffisante pour couvrir le coût du capital réglementaire.")

# --- DÉTAILS TECHNIQUES ---
with st.expander("📚 Rappels Réglementaires (S2)"):
    st.markdown(f"""
    **Le Coût du Capital (CoC) :** Fixé à 6 % par la directive, il représente le spread exigé par un investisseur pour 
    apporter les fonds propres nécessaires à la couverture des risques.
    
    **La Matrice de Corrélation :** Elle permet de calculer le SCR Diversifié en tenant compte de la faible probabilité 
    que tous les chocs de marché (Action, Spread, Immo) atteignent leur intensité maximale simultanément.
    """)
    corr_df = pd.DataFrame(
        [[1.00, 0.75, 0.75], [0.75, 1.00, 0.50], [0.75, 0.50, 1.00]],
        index=["Equity", "Spread", "Property"],
        columns=["Equity", "Spread", "Property"]
    )
    st.table(corr_df)