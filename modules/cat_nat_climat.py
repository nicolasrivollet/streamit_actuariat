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
    # Génération uniforme sur le territoire via un polygone détaillé (Rejection Sampling)
    # Permet d'éviter les points en mer avec une meilleure précision que l'hexagone.
    
    # Polygone approximatif de la France Métropolitaine (Lon, Lat)
    france_polygon = [
        (2.56, 51.10), (3.60, 50.40), (5.50, 49.50), (8.20, 49.00), # Nord-Est
        (7.50, 47.50), (6.10, 46.20), (7.10, 45.00), (7.50, 43.80), # Alpes
        (5.00, 43.20), (3.10, 42.40), (1.80, 42.40), (-1.80, 43.40), # Sud / Pyrénées
        (-1.40, 44.60), (-1.10, 46.00), (-2.10, 47.10), (-4.80, 48.40), # Atlantique / Bretagne
        (-3.90, 48.80), (-1.60, 48.60), (-1.90, 49.70), (-0.20, 49.30), (1.60, 50.10) # Manche
    ]
    
    # Algorithme Ray-Casting pour vérifier si un point est dans le polygone
    def is_inside(lon, lat):
        inside = False
        j = len(france_polygon) - 1
        for i in range(len(france_polygon)):
            xi, yi = france_polygon[i]
            xj, yj = france_polygon[j]
            intersect = ((yi > lat) != (yj > lat)) and \
                        (lon < (xj - xi) * (lat - yi) / (yj - yi) + xi)
            if intersect:
                inside = not inside
            j = i
        return inside

    lats = []
    lons = []
    
    # Génération par rejet
    while len(lats) < n:
        # Boîte englobante large autour de la France
        lat_cand = np.random.uniform(42.0, 51.5)
        lon_cand = np.random.uniform(-5.0, 8.5)
        
        if is_inside(lon_cand, lat_cand):
            lats.append(lat_cand)
            lons.append(lon_cand)
            
    lats = np.array(lats)
    lons = np.array(lons)
    
    # Détermination du type de risque (Nord = Inondation, Sud = Sécheresse)
    types = np.where(lats > 46.5, 'Inondation', 'Sécheresse')
    
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
fig_map = px.scatter_map(
    df_portfolio, 
    lat="lat", 
    lon="lon", 
    color="Perte_Attendue",
    size="TIV",
    color_continuous_scale="RdYlGn_r",
    range_color=[0, 10000], # Échelle fixe pour visualiser l'aggravation
    size_max=15, 
    zoom=4,
    map_style="open-street-map",
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
