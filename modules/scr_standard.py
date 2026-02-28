import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="SCR Formule Standard", layout="wide")

st.title("🧮 SCR Global - Formule Standard")
st.subheader("Agrégation des Risques et Diversification")

st.markdown("""
Le **Capital de Solvabilité Requis (SCR)** est calculé par une approche modulaire "Bottom-Up". 
Les risques sont calculés individuellement, puis agrégés via des **matrices de corrélation** pour tenir compte de la diversification (le fait que tous les risques ne se réalisent pas simultanément).

$$ SCR_{Global} = BSCR - Adj + SCR_{Op} $$
""")

st.divider()

# --- 1. SAISIE DES RISQUES (MODULES) ---
st.header("1. Saisie des Risques par Module")
st.info("Entrez les montants de capital requis pour chaque module de risque (avant diversification inter-modules).")

col1, col2, col3 = st.columns(3)

with col1:
    scr_market = st.number_input("SCR Marché", value=1500.0, step=100.0, help="Taux, Actions, Immo, Spread, Change, Concentration")
    scr_default = st.number_input("SCR Contrepartie", value=200.0, step=50.0, help="Défaut des réassureurs, banques, etc.")

with col2:
    scr_life = st.number_input("SCR Vie", value=800.0, step=100.0, help="Mortalité, Longévité, Rachats, Dépenses")
    scr_health = st.number_input("SCR Santé", value=100.0, step=50.0, help="SLT, Non-SLT, Catastrophe")

with col3:
    scr_nonlife = st.number_input("SCR Non-Vie", value=600.0, step=100.0, help="Primes & Réserves, Cat Nat")
    scr_intangibles = st.number_input("SCR Incorporels", value=0.0, step=10.0)

# --- 2. MATRICE DE CORRÉLATION ---
st.header("2. Agrégation (BSCR)")
st.markdown("""
Les modules sont agrégés selon la matrice de corrélation définie par le Règlement Délégué (Annexe IV).
On remarque que la corrélation entre **Vie** et **Non-Vie** est nulle (0%), offrant une forte diversification pour les assureurs composites.
""")

# Vecteur des risques
risks = np.array([scr_market, scr_default, scr_life, scr_health, scr_nonlife])
risk_labels = ["Marché", "Défaut", "Vie", "Santé", "Non-Vie"]

# Matrice de corrélation (Simplifiée sans Incorporels pour la lisibilité principale)
# Market, Default, Life, Health, Non-Life
corr_matrix = np.array([
    [1.00, 0.25, 0.25, 0.25, 0.25], # Market
    [0.25, 1.00, 0.25, 0.25, 0.50], # Default
    [0.25, 0.25, 1.00, 0.25, 0.00], # Life
    [0.25, 0.25, 0.25, 1.00, 0.00], # Health
    [0.25, 0.50, 0.00, 0.00, 1.00]  # Non-Life
])

df_corr = pd.DataFrame(corr_matrix, index=risk_labels, columns=risk_labels)

# Affichage de la matrice avec heatmap
st.write("Matrice de Corrélation (BSCR) :")
st.dataframe(df_corr.style.background_gradient(cmap="Blues", axis=None).format("{:.2f}"))

# Calcul du BSCR
# Terme quadratique : sqrt(Sum(Rho_ij * SCR_i * SCR_j))
bscr_core = np.sqrt(np.dot(risks, np.dot(corr_matrix, risks)))
bscr_total = bscr_core + scr_intangibles # Simplification : Incorporels ajoutés linéairement

sum_scr_brut = risks.sum() + scr_intangibles
diversification = sum_scr_brut - bscr_total

col_res1, col_res2 = st.columns(2)
col_res1.metric("Somme des SCR (Brut)", f"{sum_scr_brut:,.0f} €")
col_res2.metric("BSCR (Après Diversification)", f"{bscr_total:,.0f} €", delta=f"-{diversification:,.0f} € (Div.)")

# --- 3. AJUSTEMENTS & OP RISK ---
st.header("3. Passage au SCR Final")

col_adj1, col_adj2 = st.columns(2)

with col_adj1:
    st.subheader("Ajustements")
    adj_tp = st.number_input("Ajustement pour capacité d'absorption des PT (LAC TP)", value=0.0, help="Baisse de la PPB future en cas de choc")
    adj_dt = st.number_input("Ajustement pour impôts différés (LAC DT)", value=0.0, help="Économie d'impôt générée par la perte")

with col_adj2:
    st.subheader("Risque Opérationnel")
    scr_op = st.number_input("SCR Opérationnel", value=50.0, help="Souvent formule forfaitaire basée sur les Primes et Provisions")

scr_final = bscr_total - adj_tp - adj_dt + scr_op

st.divider()

# --- 4. VISUALISATION WATERFALL ---
st.header("4. Synthèse Visuelle (Waterfall)")

fig = go.Figure(go.Waterfall(
    name = "SCR", orientation = "v",
    measure = ["relative", "relative", "relative", "relative", "relative", "relative", "total", "relative", "relative", "relative", "total"],
    x = ["Marché", "Défaut", "Vie", "Santé", "Non-Vie", "Incorporels", "Somme Brute", "Diversification", "Ajustements (LAC)", "Opérationnel", "SCR Final"],
    textposition = "outside",
    text = [f"{x:,.0f}" for x in [scr_market, scr_default, scr_life, scr_health, scr_nonlife, scr_intangibles, sum_scr_brut, -diversification, -(adj_tp+adj_dt), scr_op, scr_final]],
    y = [scr_market, scr_default, scr_life, scr_health, scr_nonlife, scr_intangibles, sum_scr_brut, -diversification, -(adj_tp+adj_dt), scr_op, scr_final],
    connector = {"line":{"color":"rgb(63, 63, 63)"}},
))

fig.update_layout(
        title = "Construction du SCR (Effet de Diversification)",
        showlegend = False,
        height=500
)

st.plotly_chart(fig, use_container_width=True)

st.success(f"**Ratio de Diversification :** {diversification/sum_scr_brut:.1%} du capital économisé grâce à la diversification des risques.")
