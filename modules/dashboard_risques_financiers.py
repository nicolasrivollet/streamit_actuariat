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
    
<<<<<<< HEAD
    # Noms fictifs pour l'exemple
    names_gov = ["OAT France 2032", "Bund Allemagne 2028", "BTP Italie 2030", "Bonos Espagne 2029", "US Treasury 2025"]
    names_corp = ["TotalEnergies Bond", "LVMH Corp", "BNP Paribas Senior", "AXA Subordinated", "Danone Credit", "Orange SA"]
    names_equity = ["Air Liquide", "L'Oréal", "Schneider Electric", "Sanofi", "Airbus", "Vinci"]
    names_real = ["SCPI Bureau Paris", "OPCI Logistique", "Foncière Santé", "Immeuble La Défense"]
    
=======
>>>>>>> 93f62d02fffea217b173ca86f250829a7941c646
    data = []
    for _ in range(n_assets):
        asset_type = np.random.choice(types, p=weights)
        mv = np.random.lognormal(15, 1) # Market Value
        
        rating = "N/A"
        duration = 0.0
<<<<<<< HEAD
        name = "Cash Account"
=======
>>>>>>> 93f62d02fffea217b173ca86f250829a7941c646
        
        if "Obligations" in asset_type:
            rating = np.random.choice(ratings, p=rating_weights)
            duration = np.random.uniform(2, 15)
<<<<<<< HEAD
            name = np.random.choice(names_gov if "Gouv" in asset_type else names_corp)
=======
>>>>>>> 93f62d02fffea217b173ca86f250829a7941c646
        elif asset_type == "Cash":
            duration = 0.0
        else:
            duration = 0.0 # Simplification
<<<<<<< HEAD
            name = np.random.choice(names_equity if "Actions" in asset_type else names_real)
            
        data.append({
            "Nom de l'Actif": name,
=======
            
        data.append({
>>>>>>> 93f62d02fffea217b173ca86f250829a7941c646
            "Classe d'Actif": asset_type,
            "Valeur de Marché (M€)": mv,
            "Rating": rating,
            "Duration": duration,
            "Performance YTD (%)": np.random.normal(0.02, 0.05)
        })
        
    return pd.DataFrame(data)

df = generate_portfolio()
total_aum = df["Valeur de Marché (M€)"].sum()

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
    avg_duration = (df["Duration"] * df["Valeur de Marché (M€)"]).sum() / total_aum
    st.metric("Duration Actif", f"{avg_duration:.2f} ans")

with col4:
    # VaR Paramétrique simplifiée (99.5% 1 an)
    # Hypothèse vol portefeuille = 8%
    vol_port = 0.08
    var_995 = total_aum * vol_port * 2.58 # Quantile 99.5% N(0,1) approx
    st.metric("VaR (99.5% 1 an)", f"{var_995/1e6:,.0f} M€", delta="Capital à risque", delta_color="inverse")

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

# --- 4. ANALYSE DE SENSIBILITÉ (STRESS TESTS) ---
st.header("3. Stress Tests & Sensibilités")

col_stress1, col_stress2 = st.columns(2)

with col_stress1:
    st.subheader("Sensibilité Taux (Duration Gap)")
    liab_duration = st.slider("Duration du Passif (Cible)", 0.0, 20.0, 10.0, 0.5)
    
    gap = avg_duration - liab_duration
    impact_bps = - gap * total_aum * 0.0001 # Impact de +1bp
    
    st.metric("Duration Gap", f"{gap:.2f} ans", delta="Positif = Sur-sensible" if gap > 0 else "Négatif = Sous-sensible", delta_color="off")
    st.write(f"Impact d'une hausse des taux de **+100 bps** sur la NAV :")
    st.metric("P&L Latent", f"{impact_bps * 100 / 1e6:,.1f} M€", delta_color="inverse" if gap > 0 else "normal")

with col_stress2:
    st.subheader("Choc Actions")
    shock_equity = st.slider("Choc Boursier (%)", -50, 0, -25, 5) / 100
    
    equity_exposure = df[df["Classe d'Actif"] == "Actions"]["Valeur de Marché (M€)"].sum()
    loss_equity = equity_exposure * shock_equity
    
    st.metric("Exposition Actions", f"{equity_exposure/1e6:,.0f} M€")
    st.metric("Perte estimée", f"{loss_equity/1e6:,.1f} M€", delta_color="inverse")

st.divider()

# --- 5. TABLEAU DÉTAILLÉ ---
<<<<<<< HEAD
with st.expander("🔎 Voir le détail des lignes (Top 10)", expanded=True):
=======
with st.expander("🔎 Voir le détail des lignes (Top 10)", expanded=False):
>>>>>>> 93f62d02fffea217b173ca86f250829a7941c646
    st.dataframe(df.sort_values("Valeur de Marché (M€)", ascending=False).head(10).style.format({"Valeur de Marché (M€)": "{:,.0f}", "Performance YTD (%)": "{:.2%}", "Duration": "{:.1f}"}))
