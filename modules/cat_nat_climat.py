import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Risque Climatique & Cat Nat", layout="wide")

st.title("🌍 Risque Climatique & Catastrophes Naturelles")
st.subheader("Modélisation de l'impact du changement climatique sur le portefeuille")

st.markdown("""
Dans le cadre de l'**ORSA Climatique**, les assureurs doivent projeter l'impact du réchauffement sur leur sinistralité physique.
Ce module simule l'exposition d'un portefeuille IARD aux risques de **Sécheresse** et d'**Inondation** selon différents scénarios du GIEC (RCP).
""")

st.divider()

# --- 1. PARAMÈTRES DU SCÉNARIO ---
st.header("1. Scénario Climatique (Horizon 2050)")

col1, col2 = st.columns(2)

with col1:
    scenario = st.select_slider(
        "Scénario de Réchauffement (GIEC)",
        options=["Actuel (+1.1°C)", "Optimiste (+1.5°C)", "Intermédiaire (+2.5°C)", "Pessimiste (+4.0°C)"],
        value="Actuel (+1.1°C)"
    )

    # Facteurs d'impact (Hypothèses simplifiées EIOPA/ACPR)
    impact_map = {
        "Actuel (+1.1°C)": {"freq": 1.0, "cost": 1.0},
        "Optimiste (+1.5°C)": {"freq": 1.2, "cost": 1.15},
        "Intermédiaire (+2.5°C)": {"freq": 1.5, "cost": 1.4},
        "Pessimiste (+4.0°C)": {"freq": 2.2, "cost": 1.8}
    }
    
    factors = impact_map[scenario]
    st.info(f"**Hypothèses du modèle :**\n- Fréquence des événements : x{factors['freq']}\n- Coût moyen des sinistres : x{factors['cost']}")

with col2:
    st.metric("Impact sur la Charge Sinistre (AAL)", 
              f"+{(factors['freq'] * factors['cost'] - 1)*100:.1f}%", 
              delta="Surcoût Climatique", delta_color="inverse")

# --- 2. SIMULATION DU PORTEFEUILLE ---
st.header("2. Cartographie des Risques")

@st.cache_data
def generate_portfolio(n=500):
    # Génération de points autour de grandes agglomérations françaises
    # Cela garantit que les points sont situés sur la terre ferme (et non en mer)
    
    # Liste de villes (Lat, Lon, Type Risque Dominant)
    cities = [
        (48.8566, 2.3522, 'Inondation'),   # Paris
        (50.6292, 3.0573, 'Inondation'),   # Lille
        (47.2184, -1.5536, 'Inondation'),  # Nantes
        (48.5734, 7.7521, 'Inondation'),   # Strasbourg
        (49.4432, 1.0999, 'Inondation'),   # Rouen
        (45.7640, 4.8357, 'Sécheresse'),   # Lyon
        (43.2965, 5.3698, 'Sécheresse'),   # Marseille
        (43.6047, 1.4442, 'Sécheresse'),   # Toulouse
        (44.8378, -0.5792, 'Sécheresse'),  # Bordeaux
        (43.7102, 7.2620, 'Sécheresse')    # Nice
    ]
    
    indices = np.random.randint(0, len(cities), n)
    
    # Extraction vectorisée des coordonnées de base
    base_lats = np.array([cities[i][0] for i in indices])
    base_lons = np.array([cities[i][1] for i in indices])
    types = [cities[i][2] for i in indices]
    
    # Dispersion locale (sigma = 0.15 degrés ~ 15-20km) pour rester proche des villes
    lats = base_lats + np.random.normal(0, 0.15, n)
    lons = base_lons + np.random.normal(0, 0.15, n)
    
    df = pd.DataFrame({
        'lat': lats,
        'lon': lons,
        'TIV': np.random.lognormal(12, 0.5, n), # Total Insured Value
        'Type': types,
        'Base_Score': np.random.uniform(0, 10, n) # Score de risque intrinsèque (0-10)
    })
    return df

df_portfolio = generate_portfolio()

# Calcul du risque par police (Score simplifié)
# Le risque augmente avec le scénario
df_portfolio['Risque_Score'] = df_portfolio['Base_Score'] * factors['freq']
df_portfolio['Perte_Attendue'] = df_portfolio['TIV'] * (df_portfolio['Risque_Score'] / 1000) * factors['cost']

# Carte interactive
fig_map = px.scatter_mapbox(
    df_portfolio, 
    lat="lat", 
    lon="lon", 
    color="Perte_Attendue",
    size="TIV",
    color_continuous_scale="RdYlGn_r",
    range_color=[0, 10000], # Échelle fixe pour visualiser l'aggravation
    size_max=15, 
    zoom=4,
    mapbox_style="open-street-map",
    title="Exposition Géographique et Intensité des Pertes (Simulé)",
    hover_data={"lat": False, "lon": False, "Type": True, "TIV": ":.0f€"}
)
fig_map.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
st.plotly_chart(fig_map, use_container_width=True)

# --- 3. ANALYSE D'IMPACT ---
st.header("3. Impact sur le Ratio Sinistres à Primes (S/P)")

col_res1, col_res2 = st.columns([1, 2])

with col_res1:
    sp_initial = 0.65 # 65%
    sp_shocked = sp_initial * factors['freq'] * factors['cost']
    
    st.metric("Ratio S/P Initial", f"{sp_initial*100:.1f}%")
    st.metric("Ratio S/P Projeté 2050", f"{sp_shocked*100:.1f}%", delta=f"+{(sp_shocked-sp_initial)*100:.1f} pts", delta_color="inverse")

with col_res2:
    st.warning("""
    **Analyse Stratégique :**
    Le scénario sélectionné dégrade fortement la rentabilité technique.
    Actions correctrices possibles :
    1.  **Tarification :** Indexation des primes sur le risque climatique (Zonier).
    2.  **Souscription :** Désengagement des zones rouges (Retrait).
    3.  **Prévention :** Incitation aux mesures de protection (ex: digues).
    """)
