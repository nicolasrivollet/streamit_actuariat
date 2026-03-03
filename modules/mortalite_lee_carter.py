import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Modèle Lee-Carter", layout="wide")

st.title("💀 Modélisation de la Mortalité : Lee-Carter")
st.subheader("Projection stochastique de l'espérance de vie")

st.markdown("""
### 💡 Pourquoi ce modèle est-il crucial ?
Le risque de **longévité** (le fait que les assurés vivent plus longtemps que prévu) est un enjeu majeur pour les régimes de retraite et les assureurs versant des rentes viagères. 
Le modèle de **Lee-Carter (1992)** est devenu le standard de marché car il permet de transformer des données historiques en une projection probabiliste cohérente.

### 📐 La mécanique du modèle
Il décompose le logarithme des taux de mortalité $m_{x,t}$ (à l'âge $x$ et l'année $t$) en trois composantes interprétables :

$$ \ln(m_{x,t}) = a_x + b_x k_t + \epsilon_{x,t} $$

1.  **$a_x$ (Profil Moyen)** : La forme "standard" de la courbe de mortalité par âge (mortalité infantile, accidentelle chez les jeunes, vieillissement exponentiel).
2.  **$k_t$ (Indice Temporel)** : Un indice unique qui résume le niveau général de mortalité une année donnée. S'il baisse, la mortalité s'améliore.
3.  **$b_x$ (Sensibilité)** : Indique à quel point l'âge $x$ réagit à la baisse de $k_t$. Historiquement, les jeunes ont vu leur mortalité baisser plus vite que les centenaires.
""")

st.divider()

# --- 1. GÉNÉRATION DE DONNÉES SYNTHÉTIQUES ---
st.header("1. Visualisation de la Surface de Mortalité")
st.markdown("""
Avant de modéliser, il est essentiel de visualiser les données brutes sous forme de **surface 3D**.
On observe généralement une "vallée" qui se creuse avec le temps, signe de l'amélioration des conditions de vie et de la médecine.

*Note : Les données ci-dessous sont simulées pour l'exercice, mais reproduisent les caractéristiques réelles d'une population européenne (loi de Gompertz).*
""")

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
st.header("2. Calibration : Extraction des Paramètres")
st.markdown("""
Pour isoler les paramètres $a_x, b_x$ et $k_t$, nous utilisons une méthode d'algèbre linéaire : la **Décomposition en Valeurs Singulières (SVD)**.
Cela revient à chercher la tendance principale (1ère composante) qui explique le mieux la déformation historique de la surface de mortalité.
""")

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
    st.info("**Profil statique ($a_x$)** : On retrouve la forme classique 'en crosse de hockey'. La mortalité est élevée à la naissance, minimale vers 10 ans, puis croît exponentiellement.")

with col_p2:
    fig_bx = px.line(x=ages, y=bx, title="Paramètre b_x (Sensibilité)", labels={'x': 'Âge', 'y': 'b_x'})
    st.plotly_chart(fig_bx, use_container_width=True)
    st.info("**Sensibilité ($b_x$)** : Les pics indiquent les âges où les progrès médicaux ont été les plus rapides historiquement (souvent l'enfance et les âges moyens).")

with col_p3:
    fig_kt = px.line(x=years, y=kt, title="Paramètre k_t (Tendance)", labels={'x': 'Année', 'y': 'k_t'})
    st.plotly_chart(fig_kt, use_container_width=True)
    st.info("**Tendance ($k_t$)** : La pente négative confirme l'amélioration continue de l'espérance de vie sur la période observée.")

# --- 3. PROJECTION ---
st.header("3. Projection et Impact Actuariel")
st.markdown("""
C'est ici que l'actuariat prédictif entre en jeu. Nous modélisons l'indice $k_t$ comme une **Marche Aléatoire avec Dérive (Random Walk with Drift)**.
L'hypothèse est que la vitesse moyenne d'amélioration observée dans le passé va se poursuivre, avec une certaine volatilité.
""")

col_proj1, col_proj2 = st.columns(2)
with col_proj1:
    horizon = st.slider("Horizon de projection (années)", 10, 50, 30)
with col_proj2:
    attenuation = st.slider("Atténuation de la tendance (%)", 0, 100, 20, help="Réduit la vitesse d'amélioration future (Prudence / Ralentissement des progrès).") / 100

# Modélisation de kt comme une marche aléatoire avec dérive (Random Walk with Drift)
drift = (kt[-1] - kt[0]) / (len(kt) - 1)
drift_adj = drift * (1 - attenuation)
future_years = np.arange(years[-1] + 1, years[-1] + 1 + horizon)
kt_proj = [kt[-1] + drift_adj * (t+1) for t in range(horizon)]

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

st.success(f"📈 **Résultat :** Le modèle projette un gain d'espérance de vie de **+{e0_proj[-1] - e0_hist[-1]:.1f} ans** sur les {horizon} prochaines années.")

st.info("""
**Impact Bilan :** Pour un assureur, cette augmentation mécanique de l'espérance de vie signifie que les rentes devront être versées plus longtemps. 
Si cette dérive n'est pas anticipée dans le provisionnement (via des tables de mortalité prospectives), le bilan risque d'être sous-provisionné.
""")

st.caption("Note : L'atténuation permet de refléter l'hypothèse d'un ralentissement des progrès médicaux (plafond biologique).")
