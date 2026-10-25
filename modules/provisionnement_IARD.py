import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Provisionnement Chain-Ladder", layout="wide")

st.title("Provisionnement Non-Vie : Méthode Chain-Ladder")
st.subheader("Estimation des provisions pour sinistres à payer (IBNR)")

st.markdown("""
La méthode **Chain-Ladder** est l'algorithme standard pour projeter la charge ultime des sinistres en Assurance Non-Vie (IARD).
Elle repose sur l'hypothèse de stabilité des cadences de règlement des sinistres dans le temps.

**Objectif :** Compléter le "Triangle de Liquidation" (partie inférieure) pour estimer les montants futurs à payer.
""")

st.info("""
**Concept Clé :** En assurance IARD, le coût total d'un sinistre n'est pas connu immédiatement (ex: indemnisation corporelle longue). 
L'assureur doit donc provisionner le montant restant à payer. On distingue :
*   **Sinistres connus :** Montants déjà payés ou provisionnés dossier par dossier.
*   **IBNR (Incurred But Not Reported) :** Provision pour les sinistres tardifs ou la réévaluation des dossiers existants.
""")

st.divider()

# --- 1. DONNÉES (TRIANGLE CUMULÉ) ---
st.header("1. Triangle de Liquidation (Cumulé)")
st.markdown("""
Ce tableau présente l'historique des paiements.
*   **En ligne :** L'année de survenance du sinistre.
*   **En colonne :** L'année de développement (1 = année de l'accident, 2 = année suivante, etc.).
*   **La diagonale :** Représente la vision à date (dernier bilan). Tout ce qui est en bas à droite est inconnu (le futur).
""")

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

# Contrôles de sensibilité
with st.expander("🛠️ Paramètres de Sensibilité (Actuariat)", expanded=True):
    col_sens1, col_sens2 = st.columns(2)
    with col_sens1:
        method_avg = st.radio("Méthode de projection", ["Moyenne Historique (Tout)", "Moyenne 3 dernières années (Last 3)"], index=0, help="Permet de capturer les tendances récentes.")
    with col_sens2:
        inflation_load = st.slider("Choc Inflation Future (%)", 0.0, 15.0, 0.0, step=0.5, help="Surcharge appliquée aux flux futurs (IBNR).") / 100

st.markdown("""
Pour projeter le futur, nous devons comprendre la vitesse de liquidation passée.
On calcule un **Link Ratio** $f_j$ pour chaque année de développement $j$ :
$$ f_j = \\frac{\\sum C_{i, j+1}}{\\sum C_{i, j}} $$
C'est le coefficient multiplicateur moyen pour passer d'une année à l'autre.
""")

# Calcul des facteurs individuels (Moyenne pondérée par les volumes)
factors = []
for col in range(len(dev_years)-1):
    # Identification des lignes valides pour ce développement
    valid_rows = []
    for row in range(len(years)):
        if not np.isnan(df_triangle.iloc[row, col]) and not np.isnan(df_triangle.iloc[row, col+1]):
            valid_rows.append(row)
            
    # Filtrage selon la méthode choisie (Sensibilité)
    if "Last 3" in method_avg:
        selected_rows = valid_rows[-3:]
    else:
        selected_rows = valid_rows
        
    sum_next = df_triangle.iloc[selected_rows, col+1].sum()
    sum_curr = df_triangle.iloc[selected_rows, col].sum()
    
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

st.info("""
**Lecture :** Un facteur de 1.500 signifie que les paiements augmentent en moyenne de 50% entre ces deux années. 
Le **Facteur de Queue (Tail)** capture tout ce qui se passe après la fin du triangle (ex: réouvertures tardives).
""")

# --- 3. PROJECTION ET RÉSULTATS ---
st.header("3. Projection de la Charge Ultime & IBNR")
st.markdown("""
On applique les facteurs cumulés aux derniers montants connus (la diagonale) pour estimer le coût final (**Charge Ultime**).
La provision **IBNR** est simplement la différence entre cette estimation finale et ce qui est déjà payé.

$$ IBNR = Charge Ultime - Payé $$
""")

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
    ibnr_brut = ultimate - current_amount
    ibnr = ibnr_brut * (1 + inflation_load) # Application du choc d'inflation
    ultimate_final = current_amount + ibnr
    
    results.append({"Année": year, "Dernier Connu": current_amount, "Facteur Projection": projection_factor, "Charge Ultime": ultimate_final, "Provisions (IBNR)": ibnr})

df_res = pd.DataFrame(results)

# KPIs Globaux
total_ibnr = df_res["Provisions (IBNR)"].sum()
st.metric("Total Provisions (IBNR)", f"{total_ibnr:,.0f} €", delta="Réserve à constituer")
st.dataframe(df_res.style.format({"Dernier Connu": "{:,.0f}", "Facteur Projection": "{:.3f}", "Charge Ultime": "{:,.0f}", "Provisions (IBNR)": "{:,.0f}"}))

# Graphique
fig_res = go.Figure(go.Bar(x=df_res["Année"], y=df_res["Provisions (IBNR)"], text=df_res["Provisions (IBNR)"], texttemplate='%{text:,.0f}', marker_color='indianred'))
fig_res.update_layout(title="Constitution des Provisions par Année de Survenance", yaxis_title="Montant IBNR (€)")
st.plotly_chart(fig_res, use_container_width=True)
