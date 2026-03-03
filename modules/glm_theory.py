import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import statsmodels.api as sm
import statsmodels.formula.api as smf

st.set_page_config(page_title="Théorie GLM", layout="wide")

st.title("📈 Modèles Linéaires Généralisés (GLM)")
st.subheader("Le couteau suisse de l'actuaire")

st.markdown("""
Le **GLM (Generalized Linear Model)** est une extension de la régression linéaire simple (OLS) qui permet de modéliser des variables qui ne suivent pas une loi Normale (ex: nombre de sinistres, coût d'un sinistre).
C'est le standard de marché pour la **Tarification** et le **Provisionnement**.
""")

st.divider()

# --- 1. THÉORIE ---
st.header("1. Les 3 Composantes du GLM")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("### 1. Composante Aléatoire")
    st.write("La loi de probabilité de la variable cible $Y$.")
    st.latex(r"Y \sim \text{Famille Exponentielle}")
    st.write("Ex: Poisson, Gamma, Normale, Binomiale, Tweedie.")

with col2:
    st.warning("### 2. Composante Systématique")
    st.write("Le prédicteur linéaire construit à partir des variables explicatives $X$.")
    st.latex(r"\eta = \beta_0 + \beta_1 X_1 + ... + \beta_p X_p")

with col3:
    st.success("### 3. Fonction de Lien")
    st.write("La fonction $g$ qui relie l'espérance de $Y$ au prédicteur linéaire.")
    st.latex(r"g(E[Y]) = \eta \iff E[Y] = g^{-1}(\eta)")
    st.write("Ex: Log, Identité, Logit.")

st.divider()

# --- 2. DISTRIBUTIONS USUELLES ---
st.header("2. Distributions Actuarielles")

dist_data = {
    "Distribution": ["Poisson", "Gamma", "Tweedie", "Binomiale", "Normale"],
    "Usage Actuariel": ["Fréquence de sinistres", "Coût moyen (Sévérité)", "Prime Pure (Fréquence x Coût)", "Rétention / Churn", "Phénomènes symétriques"],
    "Fonction de Lien Canonique": ["Log", "Inverse (souvent Log en pratique)", "Log (pour p>1)", "Logit", "Identité"],
    "Variance V(µ)": ["$\mu$", "$\mu^2$", "$\mu^p$", "$\mu(1-\mu)$", "1"]
}
st.table(pd.DataFrame(dist_data))

st.divider()

# --- 3. SIMULATEUR INTERACTIF ---
st.header("3. Visualisation : Pourquoi le GLM ?")
st.markdown("Comparaison entre une régression linéaire classique (OLS) et un GLM sur des données simulées.")

col_sim1, col_sim2 = st.columns([1, 2])

with col_sim1:
    st.subheader("Paramètres")
    dist_choice = st.selectbox("Distribution", ["Poisson (Fréquence)", "Gamma (Coût)"])
    sample_size = st.slider("Nombre de points", 50, 500, 100)
    beta_0 = st.slider("Intercept (Beta 0)", 0.0, 5.0, 2.0)
    beta_1 = st.slider("Pente (Beta 1)", -0.5, 0.5, 0.1, 0.01)
    noise_level = st.slider("Niveau de bruit", 0.1, 2.0, 0.5)

with col_sim2:
    # Génération de données
    np.random.seed(42)
    X = np.linspace(0, 10, sample_size)
    
    # Prédicteur linéaire
    eta = beta_0 + beta_1 * X
    
    if dist_choice == "Poisson (Fréquence)":
        # Lien Log : mu = exp(eta)
        mu = np.exp(eta)
        y = np.random.poisson(mu)
        family = sm.families.Poisson(link=sm.families.links.log())
        title = "Modélisation de Fréquence (Loi de Poisson)"
    else:
        # Gamma : Lien Log pour assurer la positivité
        mu = np.exp(eta)
        # Paramétrage Gamma (shape k, scale theta). E[Y] = k*theta, Var[Y] = k*theta^2
        # On veut Var prop à mu^2.
        # shape = 1/dispersion.
        shape = 1 / noise_level
        scale = mu / shape
        y = np.random.gamma(shape, scale)
        family = sm.families.Gamma(link=sm.families.links.log())
        title = "Modélisation de Coût (Loi Gamma)"

    df_sim = pd.DataFrame({'X': X, 'Y': y})
    
    # Fit GLM
    glm_model = smf.glm("Y ~ X", data=df_sim, family=family).fit()
    df_sim['GLM_Pred'] = glm_model.predict(df_sim)
    
    # Fit OLS (pour comparer)
    ols_model = sm.OLS(df_sim['Y'], sm.add_constant(df_sim['X'])).fit()
    df_sim['OLS_Pred'] = ols_model.predict(sm.add_constant(df_sim['X']))
    
    # Graphique
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_sim['X'], y=df_sim['Y'], mode='markers', name='Données Simulées', marker=dict(color='gray', opacity=0.6)))
    fig.add_trace(go.Scatter(x=df_sim['X'], y=df_sim['GLM_Pred'], mode='lines', name='GLM (Adapté)', line=dict(color='green', width=3)))
    fig.add_trace(go.Scatter(x=df_sim['X'], y=df_sim['OLS_Pred'], mode='lines', name='OLS (Linéaire)', line=dict(color='red', dash='dash')))
    
    fig.update_layout(title=title, xaxis_title="Variable Explicative X", yaxis_title="Variable Cible Y")
    st.plotly_chart(fig, use_container_width=True)

# Analyse des résidus
st.subheader("Analyse des Résidus")
col_res1, col_res2 = st.columns(2)

with col_res1:
    st.markdown("**Pourquoi l'OLS échoue ?**")
    st.write("1. Il peut prédire des valeurs négatives (impossible pour une fréquence ou un coût).")
    st.write("2. Il suppose une variance constante (homoscédasticité), alors que la variance réelle augmente avec la moyenne.")

with col_res2:
    st.markdown("**Résumé du Modèle GLM (statsmodels)**")
    st.text(glm_model.summary().tables[1])