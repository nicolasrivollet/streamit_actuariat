import streamlit as st
import pandas as pd
import numpy as np

# --- LOGIQUE DE CALCUL RÉGLEMENTAIRE ---

def calculate_diversified_scr(scr_dict):
    """
    Applique la matrice de corrélation simplifiée de l'EIOPA pour le SCR Marché.
    (Exemple : Taux, Actions, Immo, Spread)
    """
    risks = list(scr_dict.keys())
    n = len(risks)
    if n == 0: return 0
    
    # Matrice de corrélation simplifiée (Standard S2)
    # Ordre : Equity, Spread, Property
    corr_matrix = np.array([
        [1.00, 0.75, 0.75], # Equity
        [0.75, 1.00, 0.50], # Spread
        [0.75, 0.50, 1.00]  # Property
    ])
    
    # On crée le vecteur des SCR composants
    # On initialise un vecteur de taille 3 (Equity, Spread, Property)
    scr_vector = np.zeros(3)
    risk_map = {"Equity": 0, "Spread": 1, "Property": 2}
    
    for risk, value in scr_dict.items():
        if risk in risk_map:
            scr_vector[risk_map[risk]] = value
            
    # Formule matricielle : sqrt(SCR^T * Corr * SCR)
    scr_total = np.sqrt(np.dot(scr_vector.T, np.dot(corr_matrix, scr_vector)))
    return scr_total

# --- INTERFACE ---

st.title("🛡️ SCR Market Asset Screener")
st.markdown("""
Cet outil permet d'évaluer l'impact prudentiel d'un nouvel investissement conformément à la **Directive Solvabilité II**. 
Il aide à la sélection d'actifs en calculant le coût du capital et la rentabilité ajustée du risque (RAROC).
""")

st.divider()

# --- SECTION 1 : CARACTÉRISTIQUES DE L'ACTIF ---
st.header("1️⃣ Caractéristiques de l'Actif")
col_a, col_b = st.columns(2)

with col_a:
    asset_name = st.text_input("Désignation de l'actif", "Obligation Corporate BBB+")
    asset_type = st.selectbox("Classe d'actif", ["Actions", "Obligations", "Immobilier"])
    nominal = st.number_input("Montant de l'investissement (€)", min_value=0, value=1000000, step=100000)

with col_b:
    yield_expected = st.number_input("Rendement annuel attendu (%)", value=4.50, step=0.1) / 100
    if asset_type == "Obligations":
        rating = st.select_slider("Rating de l'émetteur", options=["AAA", "AA", "A", "BBB", "HY"], value="BBB")
        duration = st.slider("Sensibilité (Duration modifiée)", 0.0, 20.0, 6.0)
    else:
        rating, duration = None, 0

st.divider()

# --- SECTION 2 : ANALYSE DES RISQUES SOUS-JACENTS ---
st.header("2️⃣ Calcul de la Charge en Capital (SCR)")

# Logique de calcul par module
scr_results = {}
st.markdown("### Détail des chocs de la Formule Standard")

col_text, col_calc = st.columns([2, 1])

with col_text:
    if asset_type == "Actions":
        st.write("**Module Action :** Application d'un choc de 39% (Type 1) sur la valeur de marché.")
        scr_results["Equity"] = nominal * 0.39
    
    elif asset_type == "Obligations":
        # Facteurs de stress Spread (simplifiés EIOPA)
        stress_map = {"AAA": 0.009, "AA": 0.011, "A": 0.014, "BBB": 0.025, "HY": 0.045}
        f_spread = stress_map[rating]
        st.write(f"**Module Spread :** Application d'un choc basé sur le rating (**{rating}**) et la duration (**{duration}**).")
        st.write(f"Formule : $Nominal \\times Duration \\times Factor_{{{rating}}}$")
        scr_results["Spread"] = nominal * duration * f_spread
        
    elif asset_type == "Immobilier":
        st.write("**Module Immo :** Application d'un choc forfaitaire de 25% sur la valeur d'expertise.")
        scr_results["Property"] = nominal * 0.25

with col_calc:
    for risk, val in scr_results.items():
        st.metric(f"SCR {risk}", f"{val:,.0f} €")

# --- MATRICE DE CORRÉLATION ---
st.subheader("⚙️ Effet de Diversification")
st.info("""
Le SCR Total n'est pas la somme des risques. On utilise une **matrice de corrélation** EIOPA pour tenir compte 
du fait que tous les chocs ne se produisent pas simultanément avec la même intensité.
""")

scr_div = calculate_diversified_scr(scr_results)
diversification_gain = sum(scr_results.values()) - scr_div

# --- SECTION 3 : INDICATEURS DE RENTABILITÉ ---
st.divider()
st.header("3️⃣ Indicateurs de Performance")

k_cost = 0.06 # Coût du capital hypothétique (Cost of Capital)
net_profit = nominal * yield_expected
raroc = (net_profit) / scr_div if scr_div > 0 else 0

c1, c2, c3 = st.columns(3)
c1.metric("SCR Diversifié", f"{scr_div:,.0f} €")
c2.metric("Gain de Diversification", f"{diversification_gain:,.0f} €", delta_color="normal")
c3.metric("RAROC", f"{raroc:.2%}")

# --- CONCLUSION POUR LE COMITÉ ---
st.subheader("📋 Avis de la Gestion des Risques")
if raroc > k_cost:
    st.success(f"**AVIS FAVORABLE** : Le rendement ajusté du risque ({raroc:.2%}) est supérieur au coût du capital ({k_cost:.0%}). L'investissement est créateur de valeur.")
else:
    st.warning(f"**AVIS DÉFAVORABLE** : La consommation de fonds propres est trop élevée par rapport au rendement attendu. RAROC < {k_cost:.0%}.")

with st.expander("🔍 Voir la Matrice de Corrélation utilisée"):
    corr_df = pd.DataFrame(
        [[1.00, 0.75, 0.75], [0.75, 1.00, 0.50], [0.75, 0.50, 1.00]],
        index=["Equity", "Spread", "Property"],
        columns=["Equity", "Spread", "Property"]
    )
    st.table(corr_df)