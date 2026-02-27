import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Provisionnement Chain-Ladder", layout="wide")

st.title("🔺 Provisionnement Non-Vie : Méthode Chain-Ladder")
st.subheader("Estimation des provisions pour sinistres à payer (IBNR)")

st.markdown("""
La méthode **Chain-Ladder** est l'algorithme standard pour projeter la charge ultime des sinistres en Assurance Non-Vie (IARD).
Elle repose sur l'hypothèse de stabilité des cadences de règlement des sinistres dans le temps.

**Objectif :** Compléter le "Triangle de Liquidation" (partie inférieure) pour estimer les montants futurs à payer.
""")

st.divider()

# --- 1. DONNÉES (TRIANGLE CUMULÉ) ---
st.header("1. Triangle de Liquidation (Cumulé)")

# Génération d'un triangle exemple (Années de survenance x Années de développement)
# Données fictives mais réalistes (en k€)
data = np.array([
    [3500, 6000, 7500, 8200, 8500, 8600],
    [3800, 6400, 8000, 8700, 9000, np.nan],
    [4100, 6900, 8600, 9400, np.nan, np.nan],
    [4500, 7500, 9300, np.nan, np.nan, np.nan],
    [4900, 8200, np.nan, np.nan, np.nan, np.nan],
    [5300, np.nan, np.nan, np.nan, np.nan, np.nan]
])

years = [2018, 2019, 2020, 2021, 2022, 2023]
dev_years = [1, 2, 3, 4, 5, 6]

df_triangle = pd.DataFrame(data, index=years, columns=dev_years)
df_triangle.index.name = "Année Survenance"
df_triangle.columns.name = "Année Développement"

# Affichage interactif avec Heatmap

st.write("Données historiques (Paiements cumulés) :")
st.dataframe(df_triangle.style.format("{:,.0f}", na_rep="-"))

# Heatmap pour visualiser la "masse" des paiements
fig_heat = px.imshow(df_triangle, text_auto=True, aspect="auto", color_continuous_scale="Blues", title="Heatmap des Paiements Cumulés")
st.plotly_chart(fig_heat, use_container_width=True)

# --- 2. CALCUL DES FACTEURS DE DÉVELOPPEMENT (LINK RATIOS) ---
st.header("2. Facteurs de Développement (Link Ratios)")

# Calcul des facteurs individuels (Moyenne pondérée par les volumes)
factors = []
for col in range(len(dev_years)-1):
    sum_next = 0
    sum_curr = 0
    for row in range(len(years)):
        val_curr = df_triangle.iloc[row, col]
        val_next = df_triangle.iloc[row, col+1]
        if not np.isnan(val_curr) and not np.isnan(val_next):
            sum_next += val_next
            sum_curr += val_curr
    
    if sum_curr > 0:
        factors.append(sum_next / sum_curr)
    else:
        factors.append(1.0)

# Facteur de queue (Tail Factor) interactif
tail_factor = st.slider("Facteur de Queue (Au-delà de 6 ans)", 1.0, 1.1, 1.0, step=0.01, help="Provision pour les développements tardifs au-delà de l'historique observé.")

# Facteurs cumulés (CdF - Cumulative Development Factors)
factors_all = factors + [tail_factor]
# Calcul des CdF inverses (pour projeter l'ultime à partir du courant)
# CdF[i] est le facteur pour passer de l'année i à l'ultime
cdf = []
current_prod = 1.0
# On part de la fin (Tail) et on remonte
for f in reversed(factors_all):
    current_prod *= f
    cdf.insert(0, current_prod)

# Affichage des facteurs
df_factors = pd.DataFrame([factors + [tail_factor]], columns=[f"{i}-{i+1}" for i in dev_years[:-1]] + ["Tail"])
st.write("Facteurs de passage moyens (Link Ratios) :")
st.dataframe(df_factors.style.format("{:.3f}"))

# --- 3. PROJECTION ET RÉSULTATS ---
st.header("3. Projection de la Charge Ultime & IBNR")

results = []
for i, year in enumerate(years):
    current_amount = df_triangle.iloc[i, :].max() # Dernier montant connu (diagonale)
    
    # L'année 2023 (index 5) est en développement 1. Elle doit être multipliée par le CdF correspondant au dev 1.
    # L'année 2018 (index 0) est en développement 6. Elle doit être multipliée par le CdF correspondant au dev 6 (Tail).
    
    # On récupère le facteur cumulé correspondant à l'âge actuel
    # Age actuel = nombre d'années écoulées (1 à 6) -> index dans cdf
    dev_stage_idx = len(dev_years) - 1 - i # 0 pour 2023 (dev 1), 5 pour 2018 (dev 6)
    
    # Le cdf[0] correspond au facteur total depuis le début ? Non.
    # cdf a été construit en remontant. cdf[-1] est le tail. cdf[0] est le facteur total 1->Ultime.
    # Pour 2023 (dev 1), on veut aller à l'ultime, on prend cdf[0].
    # Pour 2018 (dev 6), on a fini le triangle, on applique juste le tail (cdf[-1]).
    
    projection_factor = cdf[i] # cdf[0] applique tous les facteurs pour l'année la plus récente (2023)
    
    ultimate = current_amount * projection_factor
    ibnr = ultimate - current_amount
    
    results.append({"Année": year, "Dernier Connu": current_amount, "Facteur Projection": projection_factor, "Charge Ultime": ultimate, "Provisions (IBNR)": ibnr})

df_res = pd.DataFrame(results)

# KPIs Globaux
total_ibnr = df_res["Provisions (IBNR)"].sum()
col1, col2 = st.columns(2)
col1.metric("Total Provisions (IBNR)", f"{total_ibnr:,.0f} €", delta="Réserve à constituer")
col2.dataframe(df_res.style.format({"Dernier Connu": "{:,.0f}", "Facteur Projection": "{:.3f}", "Charge Ultime": "{:,.0f}", "Provisions (IBNR)": "{:,.0f}"}))

# Graphique
fig_res = go.Figure(go.Bar(x=df_res["Année"], y=df_res["Provisions (IBNR)"], text=df_res["Provisions (IBNR)"], texttemplate='%{text:,.0f}', marker_color='indianred'))
fig_res.update_layout(title="Constitution des Provisions par Année de Survenance", yaxis_title="Montant IBNR (€)")
st.plotly_chart(fig_res, use_container_width=True)
