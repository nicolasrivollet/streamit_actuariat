import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import statsmodels.api as sm
import statsmodels.formula.api as smf

st.set_page_config(page_title="Théorie GLM", layout="wide")

st.title("📈 Modèles Linéaires Généralisés (GLM)")
st.subheader("Le couteau suisse de l'actuaire pour la Tarification")

st.markdown("""
### Pourquoi ne pas utiliser une régression linéaire simple (OLS) ?
En assurance, nous modélisons souvent des phénomènes qui ne collent pas avec les hypothèses de la régression linéaire classique ($Y = aX + b + \epsilon$) :
1.  **Positivité :** Une fréquence ou un coût de sinistre ne peut pas être négatif. Une droite peut descendre sous zéro.
2.  **Asymétrie :** Les coûts de sinistres ont une "queue épaisse" (beaucoup de petits sinistres, quelques très gros). La loi Normale (symétrique) ne convient pas.
3.  **Variance non constante :** Plus le risque est élevé, plus la volatilité est grande (hétéroscédasticité).

Le **GLM** résout ces problèmes en généralisant le modèle.
""")

st.divider()

# --- 1. THÉORIE ---
st.header("1. La Mécanique du GLM")
st.markdown("Un GLM se définit par trois choix structurants :")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("### 1. La Loi de Probabilité\n*(Random Component)*")
    st.write("Quelle est la forme de la distribution de la variable cible $Y$ ?")
    st.markdown("""
    *   **Poisson :** Pour compter des événements (Fréquence).
    *   **Gamma :** Pour des montants positifs asymétriques (Coût Moyen).
    *   **Tweedie :** Pour la Prime Pure (mélange de zéros et de montants).
    """)

with col2:
    st.warning("### 2. Le Prédicteur Linéaire\n*(Systematic Component)*")
    st.write("On combine les variables explicatives $X$ linéairement.")
    st.latex(r"\eta = \beta_0 + \beta_1 X_1 + ... + \beta_p X_p")
    st.write("C'est le 'score' de risque brut avant transformation.")

with col3:
    st.success("### 3. La Fonction de Lien\n*(Link Function)*")
    st.write("Le pont entre le prédicteur $\eta$ (qui peut être négatif) et l'espérance $E[Y]$ (qui doit être positive).")
    st.latex(r"g(E[Y]) = \eta \iff E[Y] = g^{-1}(\eta)")
    st.write("**Exemple Log :** $E[Y] = \exp(\eta)$. Garantit un résultat positif.")

st.divider()

# --- 2. DISTRIBUTIONS USUELLES ---
st.header("2. Quelle loi pour quel usage ?")

dist_data = {
    "Distribution": ["Poisson", "Gamma", "Tweedie", "Binomiale", "Normale"],
    "Usage Actuariel": ["Fréquence de sinistres (Nb)", "Coût moyen (Sévérité €)", "Prime Pure (Fréquence x Coût)", "Rétention / Churn (Oui/Non)", "Phénomènes symétriques (Rare en IARD)"],
    "Fonction de Lien Usuelle": ["Log", "Log", "Log", "Logit", "Identité"],
    "Propriété Clé": ["Moyenne = Variance", "Écart-type proportionnel à la Moyenne", "Masse en zéro", "Probabilité entre 0 et 1", "Symétrique"]
}
st.table(pd.DataFrame(dist_data))

st.divider()

# --- 3. SIMULATEUR INTERACTIF ---
st.header("3. Visualisation : GLM vs OLS")
st.markdown("""
Observons la différence sur des données simulées.
*   **Scénario :** La fréquence de sinistres augmente exponentiellement avec une variable de risque $X$ (ex: Puissance du véhicule).
*   **Problème de l'OLS :** Il trace une droite. Il va sous-estimer le risque élevé et surestimer le risque faible (voire prédire du négatif).
""")

col_sim1, col_sim2 = st.columns([1, 2])

with col_sim1:
    st.subheader("Paramètres de Simulation")
    dist_choice = st.selectbox("Type de Phénomène", ["Poisson (Fréquence)", "Gamma (Coût Moyen)"])
    sample_size = st.slider("Nombre d'observations", 50, 1000, 200)
    st.latex(r"Y = \exp(\beta_0 + \beta_1 X)")
    beta_0 = st.slider("Niveau de base (Intercept)", 0.0, 3.0, 1.0, 0.1)
    beta_1 = st.slider("Sensibilité à X (Pente)", 0.0, 0.5, 0.2, 0.01)
    noise_level = st.slider("Dispersion (Bruit)", 0.1, 2.0, 0.5)

with col_sim2:
    # Génération de données
    np.random.seed(42)
    X = np.linspace(0, 10, sample_size)
    
    # Prédicteur linéaire
    eta = beta_0 + beta_1 * X
    
    if "Poisson" in dist_choice:
        # Lien Log : mu = exp(eta)
        mu = np.exp(eta)
        y = np.random.poisson(mu)
        family = sm.families.Poisson(link=sm.families.links.log())
        title = "Modélisation de Fréquence (Loi de Poisson)"
        y_label = "Nombre de Sinistres"
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
        y_label = "Coût du Sinistre (€)"

    df_sim = pd.DataFrame({'X': X, 'Y': y})
    
    # Fit GLM
    try:
        glm_model = smf.glm("Y ~ X", data=df_sim, family=family).fit()
        df_sim['GLM_Pred'] = glm_model.predict(df_sim)
    except:
        st.error("Erreur de convergence du GLM (données trop bruitées ou inadaptées).")
        df_sim['GLM_Pred'] = 0
    
    # Fit OLS (pour comparer)
    ols_model = sm.OLS(df_sim['Y'], sm.add_constant(df_sim['X'])).fit()
    df_sim['OLS_Pred'] = ols_model.predict(sm.add_constant(df_sim['X']))
    
    # Graphique
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_sim['X'], y=df_sim['Y'], mode='markers', name='Observations', marker=dict(color='gray', opacity=0.5)))
    fig.add_trace(go.Scatter(x=df_sim['X'], y=df_sim['GLM_Pred'], mode='lines', name='GLM (Log-Link)', line=dict(color='green', width=4)))
    fig.add_trace(go.Scatter(x=df_sim['X'], y=df_sim['OLS_Pred'], mode='lines', name='Régression Linéaire (OLS)', line=dict(color='red', dash='dash', width=3)))
    
    fig.update_layout(title=title, xaxis_title="Variable de Risque X", yaxis_title=y_label, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# Analyse des résidus
st.subheader("4. Interprétation des Résultats")
col_res1, col_res2 = st.columns(2)

with col_res1:
    st.markdown("### 🔍 Pourquoi le GLM gagne ?")
    st.markdown(r"""
    1.  **Courbure :** Le GLM (courbe verte) épouse la forme exponentielle des données. L'OLS (droite rouge) est trop rigide.
    2.  **Positivité :** Si vous baissez l'intercept ($\beta_0$), la droite rouge peut prédire des valeurs négatives pour $X$ faible. Le GLM tendra vers 0 sans jamais le traverser.
    3.  **Coefficients Multiplicatifs :**
        *   Dans un GLM Log-Link : $Y = \exp(\beta_0 + \beta_1 X) = \exp(\beta_0) \times \exp(\beta_1)^X$.
        *   Augmenter $X$ de 1 multiplie le risque par un facteur constant (Relativité). C'est la base de la tarification actuarielle.
    """)

with col_res2:
    st.markdown("### 📊 Sortie du Modèle (Statsmodels)")
    if 'glm_model' in locals():
        st.text(glm_model.summary().tables[1])
        st.caption("P-value < 0.05 indique que la variable est significative.")
