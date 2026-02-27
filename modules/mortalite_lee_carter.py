import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Modèle Lee-Carter", layout="wide")

st.title("💀 Modélisation de la Mortalité : Lee-Carter")
st.subheader("Projection stochastique de l'espérance de vie")

st.markdown("""
Le modèle de **Lee-Carter (1992)** est le standard actuariel pour projeter les taux de mortalité futurs.
Il décompose le logarithme des taux de mortalité $m_{x,t}$ (à l'âge $x$ et l'année $t$) en trois composantes :

$$ \ln(m_{x,t}) = a_x + b_x k_t + \epsilon_{x,t} $$

*   **$a_x$** : La structure par âge moyenne de la mortalité.
*   **$k_t$** : L'indice de mortalité temporel (tendance générale, souvent décroissante).
*   **$b_x$** : La sensibilité de chaque âge aux variations de $k_t$.
""")

st.divider()

# --- 1. GÉNÉRATION DE DONNÉES SYNTHÉTIQUES ---
st.header("1. Données Historiques (Simulées)")

@st.cache_data
def generate_mortality_data(years, ages):
    # Simulation simplifiée type Gompertz avec amélioration temporelle
    # ln(m_x) ~ A + B*x
    # Amélioration : le niveau baisse avec le temps
    
    n_years = len(years)
    n_ages = len(ages)
    
    # Paramètres Gompertz de base
    A = -9.0
    B = 0.08
    
    # Tendance temporelle (k_t théorique) : baisse linéaire
    kt_sim = np.linspace(10, -10, n_years)
    
    # Sensibilité par âge (b_x théorique) : les jeunes s'améliorent plus vite que les très vieux
    bx_sim = np.linspace(0.15, 0.05, n_ages)
    
    # Construction de la matrice
    log_mx = np.zeros((n_ages, n_years))
    
    for t_idx, t in enumerate(years):
        for x_idx, x in enumerate(ages):
            # Base Gompertz + Effet Lee-Carter + Bruit
            base = A + B * x
            improvement = bx_sim[x_idx] * kt_sim[t_idx]
            noise = np.random.normal(0, 0.05)
            log_mx[x_idx, t_idx] = base + improvement + noise
            
    mx = np.exp(log_mx)
    return pd.DataFrame(mx, index=ages, columns=years)

years = np.arange(1980, 2021)
ages = np.arange(0, 101)
df_mx = generate_mortality_data(years, ages)

col1, col2 = st.columns([1, 2])
with col1:
    st.write("Extrait de la table de mortalité ($q_x$ ou $m_x$) :")
    st.dataframe(df_mx.style.format("{:.4f}"))

with col2:
    fig_surface = go.Figure(data=[go.Surface(z=df_mx.values, x=years, y=ages, colorscale='Viridis')])
    fig_surface.update_layout(title="Surface de Mortalité Historique", scene=dict(xaxis_title="Année", yaxis_title="Âge", zaxis_title="Taux mx"), height=500)
    st.plotly_chart(fig_surface, use_container_width=True)

# --- 2. CALIBRATION (SVD) ---
st.header("2. Calibration du Modèle (SVD)")

# 1. Calcul de ax (moyenne temporelle du log mortalité)
log_mx_matrix = np.log(df_mx.values)
ax = log_mx_matrix.mean(axis=1)

# 2. Centrage de la matrice
centered_matrix = log_mx_matrix - ax[:, np.newaxis]

# 3. SVD
U, S, Vt = np.linalg.svd(centered_matrix, full_matrices=False)

# 4. Extraction des facteurs (1ère composante principale)
# Lee-Carter impose des contraintes : sum(bx) = 1 et sum(kt) = 0
bx_unscaled = U[:, 0]
kt_unscaled = Vt[0, :] * S[0]

sum_bx = np.sum(bx_unscaled)
bx = bx_unscaled / sum_bx
kt = kt_unscaled * sum_bx

# Visualisation des paramètres
col_p1, col_p2, col_p3 = st.columns(3)

with col_p1:
    fig_ax = px.line(x=ages, y=ax, title="Paramètre a_x (Niveau moyen)", labels={'x': 'Âge', 'y': 'a_x'})
    st.plotly_chart(fig_ax, use_container_width=True)
    st.caption("Profil de mortalité moyen : faible mortalité infantile, puis croissance exponentielle (Gompertz).")

with col_p2:
    fig_bx = px.line(x=ages, y=bx, title="Paramètre b_x (Sensibilité)", labels={'x': 'Âge', 'y': 'b_x'})
    st.plotly_chart(fig_bx, use_container_width=True)
    st.caption("Indique quels âges bénéficient le plus de l'amélioration de la mortalité.")

with col_p3:
    fig_kt = px.line(x=years, y=kt, title="Paramètre k_t (Tendance)", labels={'x': 'Année', 'y': 'k_t'})
    st.plotly_chart(fig_kt, use_container_width=True)
    st.caption("Indice de mortalité : une pente négative indique une amélioration globale.")

# --- 3. PROJECTION ---
st.header("3. Projection Future")

horizon = st.slider("Horizon de projection (années)", 10, 50, 30)

# Modélisation de kt comme une marche aléatoire avec dérive (Random Walk with Drift)
drift = (kt[-1] - kt[0]) / (len(kt) - 1)
future_years = np.arange(years[-1] + 1, years[-1] + 1 + horizon)
kt_proj = [kt[-1] + drift * (t+1) for t in range(horizon)]

# Reconstruction de la surface projetée
log_mx_proj = ax[:, np.newaxis] + np.outer(bx, kt_proj)
mx_proj = np.exp(log_mx_proj)

# Affichage Gain Espérance de vie (simplifié à la naissance)
def calc_e0(mx_col):
    return np.sum(np.cumprod(1 - (1 - np.exp(-mx_col)))) + 0.5

e0_hist = [calc_e0(df_mx[y].values) for y in years]
e0_proj = [calc_e0(mx_proj[:, t]) for t in range(horizon)]

fig_e0 = go.Figure()
fig_e0.add_trace(go.Scatter(x=years, y=e0_hist, name="Historique", line=dict(color='blue')))
fig_e0.add_trace(go.Scatter(x=future_years, y=e0_proj, name="Projection Lee-Carter", line=dict(color='orange', dash='dash')))
fig_e0.update_layout(title="Projection de l'Espérance de Vie à la naissance (e0)", xaxis_title="Année", yaxis_title="Espérance de vie (ans)")
st.plotly_chart(fig_e0, use_container_width=True)

st.success(f"Gain d'espérance de vie projeté sur {horizon} ans : +{e0_proj[-1] - e0_hist[-1]:.1f} ans")
