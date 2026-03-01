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

# --- SECTION 3 : EFFICACITÉ DU CAPITAL (SOLVABILITÉ) ---
st.divider()
st.header("3️⃣ Efficacité du Capital & Solvabilité")

# Analyse Solvabilité (Asset vs SCR)
# L'actif entre au bilan : il augmente les Fonds Propres (Asset Side) de sa valeur nominale.
# Il augmente le SCR de 'scr_div'.
apport_fp = nominal
surplus_solvabilite = apport_fp - scr_div
ratio_couverture_implicite = apport_fp / scr_div if scr_div > 0 else float('inf')

# Affichage des métriques clés
m1, m2, m3 = st.columns(3)
m1.metric("SCR Consommé", f"{scr_div:,.0f} €", delta="Exigence de Capital", delta_color="inverse")
m2.metric("Apport Fonds Propres", f"{apport_fp:,.0f} €", help="Valeur de marché de l'actif (Contribution aux FP)")
m3.metric("Ratio de Couverture Implicite", f"{ratio_couverture_implicite:.0%}", delta="Densité Solvabilité")

# --- VISUALISATION ---
col_plot, col_analysis = st.columns([1.5, 1])

with col_plot:
    # Jauge de densité solvabilité
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = ratio_couverture_implicite * 100,
        title = {'text': "Ratio Asset / SCR (%)", 'font': {'size': 16}},
        gauge = {
            'axis': {'range': [0, 400]},
            'bar': {'color': "#1E88E5"},
            'steps': [
                {'range': [0, 100], 'color': "#FFCDD2"}, # Sous-capitalisé
                {'range': [100, 400], 'color': "#C8E6C9"}], # Sur-capitalisé
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 100}}))
    fig_gauge.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig_gauge, use_container_width=True)

with col_analysis:
    st.subheader("Analyse Stratégique")
    st.write(f"""
    Cet investissement apporte **{apport_fp:,.0f} €** de valeur d'actif pour une consommation de capital de **{scr_div:,.0f} €**.
    
    Il génère donc un **surplus de solvabilité brut de {surplus_solvabilite:,.0f} €**.
    """)
    
    if ratio_couverture_implicite > 1.5:
        st.success("**PROFIL SOLVABILITÉ : ROBUSTE**")
        st.write("L'actif est 'dense' en capital : il apporte beaucoup plus de fonds propres qu'il ne consomme de SCR (> 150%).")
    elif ratio_couverture_implicite > 1.0:
        st.warning("**PROFIL SOLVABILITÉ : CORRECT**")
        st.write("L'actif couvre sa propre exigence de capital, mais avec une marge limitée.")
    else:
        st.error("**PROFIL SOLVABILITÉ : DILUTIF**")
        st.write("Attention : L'actif consomme plus de SCR qu'il n'apporte de valeur (cas rare, ex: dérivés ou levier).")

# --- DÉTAILS TECHNIQUES ---
with st.expander("📚 Rappels Réglementaires (S2)"):
    st.markdown(f"""
    **Philosophie du Ratio Implicite :**
    Plutôt que de comparer le rendement au Coût du Capital (CoC), il est souvent plus pertinent pour le pilotage du bilan de vérifier la **densité en solvabilité** de l'actif.
    
    $$ \\text{Ratio} = \\frac{\\text{Valeur de Marché (Apport FP)}}{\\text{SCR Consommé}} $$
    
    Si ce ratio est supérieur au ratio de solvabilité cible de la compagnie (ex: 200%), l'investissement est **relutif** (il améliore le ratio global).
    
    **La Matrice de Corrélation :** Elle permet de calculer le SCR Diversifié en tenant compte de la faible probabilité 
    que tous les chocs de marché (Action, Spread, Immo) atteignent leur intensité maximale simultanément.
    """)
    corr_df = pd.DataFrame(
        [[1.00, 0.75, 0.75], [0.75, 1.00, 0.50], [0.75, 0.50, 1.00]],
        index=["Equity", "Spread", "Property"],
        columns=["Equity", "Spread", "Property"]
    )
    st.table(corr_df)