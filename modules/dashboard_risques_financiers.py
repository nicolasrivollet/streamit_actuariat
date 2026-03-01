import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Tableau de Bord Risques Financiers", layout="wide")

st.title("📊 Tableau de Bord des Risques Financiers")
st.subheader("Suivi de l'Allocation d'Actifs et des Indicateurs de Risque de Marché")

st.markdown("""
Ce tableau de bord permet au Risk Manager de surveiller l'exposition du portefeuille d'actifs, 
la qualité de crédit et la sensibilité aux chocs de marché (Taux, Actions).
""")

st.divider()

# --- 1. GÉNÉRATION DE DONNÉES (PORTEFEUILLE FICTIF) ---
@st.cache_data
def generate_portfolio():
    np.random.seed(42)
    n_assets = 100
    
    types = ['Obligations Gouv.', 'Obligations Corp.', 'Actions', 'Immobilier', 'Cash']
    weights = [0.40, 0.30, 0.15, 0.10, 0.05]
    
    ratings = ['AAA', 'AA', 'A', 'BBB', 'BB', 'B']
    rating_weights = [0.2, 0.3, 0.3, 0.15, 0.04, 0.01]
    
    # Noms fictifs pour l'exemple
    names_gov = ["OAT France 2032", "Bund Allemagne 2028", "BTP Italie 2030", "Bonos Espagne 2029", "US Treasury 2025"]
    names_corp = ["TotalEnergies Bond", "LVMH Corp", "BNP Paribas Senior", "AXA Subordinated", "Danone Credit", "Orange SA"]
    names_equity = ["Air Liquide", "L'Oréal", "Schneider Electric", "Sanofi", "Airbus", "Vinci"]
    names_real = ["SCPI Bureau Paris", "OPCI Logistique", "Foncière Santé", "Immeuble La Défense"]
    
    data = []
    for _ in range(n_assets):
        asset_type = np.random.choice(types, p=weights)
        mv = np.random.lognormal(15, 1) # Market Value
        
        rating = "N/A"
        duration = 0.0
        name = "Cash Account"
        
        if "Obligations" in asset_type:
            rating = np.random.choice(ratings, p=rating_weights)
            duration = np.random.uniform(2, 15)
            name = np.random.choice(names_gov if "Gouv" in asset_type else names_corp)
        elif asset_type == "Cash":
            duration = 0.0
        else:
            duration = 0.0 # Simplification
            name = np.random.choice(names_equity if "Actions" in asset_type else names_real)
            
        data.append({
            "Nom de l'Actif": name,
            "Classe d'Actif": asset_type,
            "Valeur de Marché (M€)": mv,
            "Rating": rating,
            "Duration": duration,
            "Performance YTD (%)": np.random.normal(0.02, 0.05)
        })
        
    return pd.DataFrame(data)

df = generate_portfolio()
total_aum = df["Valeur de Marché (M€)"].sum()

# --- PARAMÈTRES DE RISQUE ---
st.header("⚙️ Paramètres de Risque")
col_p1, col_p2 = st.columns(2)

with col_p1:
    liab_duration = st.slider("Duration Passif (Cible)", 0.0, 20.0, 10.0, 0.5)

with col_p2:
    sa = st.slider("Ajustement Symétrique (SA)", -10.0, 10.0, 0.0, 0.1, help="Mécanisme contracyclique (-10% à +10%)") / 100

# --- MOTEUR DE CALCUL SCR (PRE-CALCUL) ---
# 1. Actions (Choc Type 1 + SA)
equity_exposure = df[df["Classe d'Actif"] == "Actions"]["Valeur de Marché (M€)"].sum()
scr_equity = equity_exposure * (0.39 + sa)

# 2. Immobilier (Choc 25%)
prop_exposure = df[df["Classe d'Actif"] == "Immobilier"]["Valeur de Marché (M€)"].sum()
scr_property = prop_exposure * 0.25

# 3. Spread (Tableau standard)
def calc_spread_scr(row):
    if "Obligations" not in row["Classe d'Actif"]: return 0
    factors = {'AAA': 0.009, 'AA': 0.011, 'A': 0.014, 'BBB': 0.025, 'BB': 0.045, 'B': 0.075}
    f = factors.get(row['Rating'], 0.045)
    return row["Valeur de Marché (M€)"] * row["Duration"] * f

df['SCR_Spread'] = df.apply(calc_spread_scr, axis=1)
scr_spread = df['SCR_Spread'].sum()

# 4. Taux (Proxy Duration Gap)
avg_duration = (df["Duration"] * df["Valeur de Marché (M€)"]).sum() / total_aum
gap = avg_duration - liab_duration
scr_rate = abs(gap * total_aum * 0.01) # Proxy 1%

# 5. Agrégation (Matrice Corrélation Simplifiée)
scr_vec = np.array([scr_equity, scr_property, scr_spread, scr_rate])
corr_mat = np.array([[1.0, 0.75, 0.75, 0.5], [0.75, 1.0, 0.5, 0.5], [0.75, 0.5, 1.0, 0.5], [0.5, 0.5, 0.5, 1.0]])
scr_market = np.sqrt(np.dot(scr_vec, np.dot(corr_mat, scr_vec)))

# --- 2. KPIS GLOBAUX ---
st.header("1. Indicateurs Clés (KPIs)")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Encours Total (AUM)", f"{total_aum/1e6:,.0f} M€")

with col2:
    avg_perf = (df["Performance YTD (%)"] * df["Valeur de Marché (M€)"]).sum() / total_aum
    st.metric("Performance YTD", f"{avg_perf*100:.2f}%", delta=f"{avg_perf*100 - 1.5:.2f} pts vs Budget")

with col3:
    # Duration moyenne pondérée (sur le total, incluant actions à 0)
    st.metric("Duration Actif", f"{avg_duration:.2f} ans")

with col4:
    st.metric("SCR Marché (99.5%)", f"{scr_market/1e6:,.0f} M€", delta="Capital Réglementaire", delta_color="inverse",
              help="Estimation du SCR Marché selon la Formule Standard (agrégation des chocs Actions, Immo, Spread, Taux).")

st.divider()

# --- 3. ALLOCATION D'ACTIFS ---
st.header("2. Allocation Stratégique")

col_alloc1, col_alloc2 = st.columns([1, 1])

with col_alloc1:
    # Pie Chart
    fig_pie = px.pie(df, values='Valeur de Marché (M€)', names="Classe d'Actif", title="Répartition par Classe d'Actif", hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

with col_alloc2:
    # Bar Chart Ratings (Obligations uniquement)
    df_bonds = df[df["Classe d'Actif"].str.contains("Obligations")]
    df_ratings = df_bonds.groupby("Rating")["Valeur de Marché (M€)"].sum().reset_index()
    
    # Ordre des ratings
    rating_order = ['AAA', 'AA', 'A', 'BBB', 'BB', 'B']
    
    fig_bar = px.bar(df_ratings, x="Rating", y="Valeur de Marché (M€)", 
                     category_orders={"Rating": rating_order},
                     title="Qualité de Crédit (Obligations)", color="Rating",
                     color_discrete_sequence=px.colors.sequential.Blues_r)
    st.plotly_chart(fig_bar, use_container_width=True)

# --- 4. ANALYSE DE SENSIBILITÉ (SOLVABILITÉ II) ---
st.header("3. Impact des Chocs Solvabilité II (Bicentenaires)")
st.markdown("Estimation des pertes de valeur (SCR Marché) selon les calibrages de la Formule Standard (VaR 99.5%).")

col_stress1, col_stress2 = st.columns(2)

with col_stress1:
    st.subheader("Choc Actions (Type 1)")
    sa = st.slider("Ajustement Symétrique (SA)", -10.0, 10.0, 0.0, 0.1, help="Mécanisme contracyclique (-10% à +10%)") / 100
    shock_equity_s2 = 0.39 + sa
    
    equity_exposure = df[df["Classe d'Actif"] == "Actions"]["Valeur de Marché (M€)"].sum()
    loss_equity_s2 = equity_exposure * shock_equity_s2
    
    st.metric("Exposition Actions", f"{equity_exposure/1e6:,.0f} M€")
    st.metric("SCR Actions (Est.)", f"{loss_equity_s2/1e6:,.1f} M€", delta=f"-{shock_equity_s2*100:.1f}%", delta_color="inverse")

    st.subheader("Choc Immobilier")
    prop_exposure = df[df["Classe d'Actif"] == "Immobilier"]["Valeur de Marché (M€)"].sum()
    scr_prop = prop_exposure * 0.25
    st.metric("SCR Immobilier", f"{scr_prop/1e6:,.1f} M€", delta="-25%", delta_color="inverse")

with col_stress2:
    st.subheader("Choc Spread (Crédit)")
    # Calcul détaillé par ligne pour le Spread
    def calc_spread_scr(row):
        if "Obligations" not in row["Classe d'Actif"]: return 0
        # Facteurs simplifiés S2 (Tableau A - Obligations)
        factors = {'AAA': 0.009, 'AA': 0.011, 'A': 0.014, 'BBB': 0.025, 'BB': 0.045, 'B': 0.075}
        f = factors.get(row['Rating'], 0.0)
        return row["Valeur de Marché (M€)"] * row["Duration"] * f

    df['SCR_Spread'] = df.apply(calc_spread_scr, axis=1)
    scr_spread_total = df['SCR_Spread'].sum()
    st.metric("SCR Spread (Est.)", f"{scr_spread_total/1e6:,.1f} M€", delta="Risque de Crédit", delta_color="inverse")

    st.subheader("Choc Taux (Simplifié)")
    liab_duration = st.slider("Duration Passif", 0.0, 20.0, 10.0, 0.5)
    gap = avg_duration - liab_duration
    # Proxy : Choc parallèle de +/- 1% (100bps) pour estimer l'ordre de grandeur du SCR Taux
    impact_nav = abs(gap * total_aum * 0.01)
    
    st.metric("Duration Gap", f"{gap:.2f} ans")
    st.metric("SCR Taux (Proxy +/- 1%)", f"{impact_nav/1e6:,.1f} M€", delta_color="inverse", help="Estimation simplifiée basée sur le Duration Gap.")

st.divider()

# --- 5. TABLEAU DÉTAILLÉ ---
with st.expander("🔎 Voir le détail des lignes (Top 10)", expanded=True):
    st.dataframe(df.sort_values("Valeur de Marché (M€)", ascending=False).head(10).style.format({"Valeur de Marché (M€)": "{:,.0f}", "Performance YTD (%)": "{:.2%}", "Duration": "{:.1f}"}))
