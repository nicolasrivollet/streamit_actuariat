import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import PoissonRegressor
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline

st.set_page_config(page_title="Tarification Auto : GLM vs ML", layout="wide")

st.title("🤖 Tarification Non-Vie : GLM vs Machine Learning")
st.subheader("Comparaison des approches pour la fréquence de sinistres")

st.markdown("""
En tarification IARD (Auto/Habitation), l'actuaire cherche à prédire la **fréquence des sinistres** ($\lambda$).
*   **Approche Classique (GLM) :** Modèle linéaire généralisé (Loi de Poisson). Très interprétable (structure multiplicative), mais capture mal les non-linéarités.
*   **Approche Moderne (Machine Learning) :** Gradient Boosting (GBM). Capture les interactions complexes ("Effet jeune conducteur sur voiture puissante"), mais effet "Boîte Noire".
""")

st.divider()

# --- 1. GÉNÉRATION DU DATASET ---
st.header("1. Simulation du Portefeuille Auto")

@st.cache_data
def generate_data(n_rows=10000):
    np.random.seed(42)
    
    # Features
    age = np.random.randint(18, 85, n_rows)
    power = np.random.randint(4, 15, n_rows) # Chevaux fiscaux
    density = np.random.choice(['Rural', 'Urbain', 'Paris'], n_rows, p=[0.4, 0.4, 0.2])
    
    df = pd.DataFrame({'Age': age, 'Puissance': power, 'Zone': density})
    
    # Vraie loi de risque (Ground Truth)
    # 1. Effet Age : Jeunes très risqués, Vieux un peu risqués (Forme en U)
    risk_age = 0.2 * np.exp(-0.1 * (age - 18)) + 0.05 * np.exp(0.02 * (age - 50))
    
    # 2. Effet Puissance : Risque augmente avec la puissance
    risk_power = 0.05 * np.exp(0.1 * power)
    
    # 3. Effet Zone
    risk_zone = df['Zone'].map({'Rural': 0.8, 'Urbain': 1.2, 'Paris': 1.5})
    
    # 4. Interaction (Non-linéarité) : Jeune + Puissante = Risque explosif
    interaction = np.where((age < 25) & (power > 10), 2.0, 1.0)
    
    # Lambda final (Fréquence espérée)
    true_lambda = risk_age * risk_power * risk_zone * interaction
    
    # Simulation des sinistres (Loi de Poisson)
    df['Sinistres'] = np.random.poisson(true_lambda)
    df['Exposition'] = 1.0 # Simplification : tout le monde est là 1 an
    df['Frequence_Obs'] = df['Sinistres'] / df['Exposition']
    
    return df

df = generate_data(n_rows=5000)

col1, col2 = st.columns([1, 2])
with col1:
    st.write("Aperçu des données :")
    st.dataframe(df.head(10))
    st.caption(f"Nombre de polices : {len(df)}")
    st.caption(f"Fréquence moyenne : {df['Sinistres'].mean():.2%}")

with col2:
    # Graphique Fréquence par Age (Empirique)
    df_age = df.groupby('Age')['Frequence_Obs'].mean().reset_index()
    fig_obs = px.scatter(df_age, x='Age', y='Frequence_Obs', title="Fréquence Observée par Âge (Données Brutes)", trendline="lowess")
    st.plotly_chart(fig_obs, use_container_width=True)

st.divider()

# --- 2. MODÉLISATION ---
st.header("2. Entraînement des Modèles")

col_m1, col_m2 = st.columns(2)

with col_m1:
    st.subheader("🔵 GLM (Poisson)")
    st.write("Régression de Poisson standard.")
    # Pipeline GLM
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(drop='first'), ['Zone']),
            ('num', 'passthrough', ['Age', 'Puissance'])
        ]
    )
    glm = make_pipeline(preprocessor, PoissonRegressor(alpha=1e-12, max_iter=300))
    glm.fit(df[['Age', 'Puissance', 'Zone']], df['Sinistres'])
    df['Pred_GLM'] = glm.predict(df[['Age', 'Puissance', 'Zone']])
    st.success("Modèle GLM calibré.")

with col_m2:
    st.subheader("🟢 Machine Learning (GBM)")
    st.write("Histogram Gradient Boosting (similaire à XGBoost/LightGBM).")
    # Pipeline GBM (Gère nativement les catégories et non-linéarités)
    # On doit juste encoder les catégories proprement pour sklearn
    preprocessor_gbm = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), ['Zone']),
            ('num', 'passthrough', ['Age', 'Puissance'])
        ]
    )
    gbm = make_pipeline(preprocessor_gbm, HistGradientBoostingRegressor(loss='poisson', max_iter=100))
    gbm.fit(df[['Age', 'Puissance', 'Zone']], df['Sinistres'])
    df['Pred_GBM'] = gbm.predict(df[['Age', 'Puissance', 'Zone']])
    st.success("Modèle GBM calibré.")

# --- 3. COMPARAISON DES RÉSULTATS ---
st.header("3. Analyse Comparative")

tab_res1, tab_res2 = st.tabs(["Analyse par Âge (Non-linéarité)", "Interaction (Jeune & Puissant)"])

with tab_res1:
    st.markdown("Le GLM lisse la courbe (relation log-linéaire), tandis que le GBM capture mieux les ruptures (ex: sur-risque jeunes conducteurs).")
    
    # Agrégation par âge
    df_plot = df.groupby('Age')[['Frequence_Obs', 'Pred_GLM', 'Pred_GBM']].mean().reset_index()
    
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Scatter(x=df_plot['Age'], y=df_plot['Frequence_Obs'], mode='markers', name='Observé', marker=dict(color='gray', opacity=0.5)))
    fig_comp.add_trace(go.Scatter(x=df_plot['Age'], y=df_plot['Pred_GLM'], mode='lines', name='GLM (Classique)', line=dict(color='blue', width=3)))
    fig_comp.add_trace(go.Scatter(x=df_plot['Age'], y=df_plot['Pred_GBM'], mode='lines', name='GBM (Machine Learning)', line=dict(color='green', width=3)))
    
    fig_comp.update_layout(title="Ajustement du modèle sur l'Âge", xaxis_title="Âge du conducteur", yaxis_title="Fréquence Sinistres")
    st.plotly_chart(fig_comp, use_container_width=True)

with tab_res2:
    st.markdown("Le GBM excelle à détecter les **interactions** (ex: Jeune conducteur + Voiture Puissante) que le GLM standard rate (sauf si on ajoute manuellement des variables croisées).")
    
    # Création d'une catégorie pour l'analyse
    df['Segment'] = np.where((df['Age'] < 25) & (df['Puissance'] > 10), "Jeune & Sportive (Risqué)", "Autres")
    
    df_seg = df.groupby('Segment')[['Frequence_Obs', 'Pred_GLM', 'Pred_GBM']].mean().reset_index()
    
    # Melt pour plotly express
    df_melt = df_seg.melt(id_vars='Segment', value_vars=['Frequence_Obs', 'Pred_GLM', 'Pred_GBM'], var_name='Modèle', value_name='Fréquence')
    
    fig_bar = px.bar(df_melt, x='Segment', y='Fréquence', color='Modèle', barmode='group', 
                     title="Capacité à capturer le sur-risque 'Jeune & Sportive'",
                     color_discrete_map={'Frequence_Obs': 'gray', 'Pred_GLM': 'blue', 'Pred_GBM': 'green'})
    st.plotly_chart(fig_bar, use_container_width=True)