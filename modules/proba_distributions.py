import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import poisson, nbinom, binom, norm, lognorm, gamma, pareto

st.set_page_config(page_title="Lois de Probabilités", layout="wide")

st.title("🎲 Principales Lois de Probabilités en Actuariat")
st.subheader("Fondamentaux pour la modélisation des risques")

st.markdown("""
L'actuaire modélise l'incertitude. Pour cela, il s'appuie sur des distributions de probabilité spécifiques selon la nature du risque :
*   **Fréquence :** Combien de sinistres vont survenir ? (Lois Discrètes)
*   **Sévérité :** Quel sera le coût d'un sinistre ? (Lois Continues)
*   **Queues épaisses :** Comment modéliser les événements extrêmes ? (Lois à queue lourde)
""")

st.divider()

tab_discrete, tab_continuous = st.tabs(["Lois Discrètes (Fréquence)", "Lois Continues (Sévérité)"])

with tab_discrete:
    st.header("Modélisation de la Fréquence")
    
    dist_type = st.selectbox("Choisir une loi", ["Poisson", "Binomiale Négative", "Binomiale"])
    
    col_param, col_viz = st.columns([1, 2])
    
    if dist_type == "Poisson":
        with col_param:
            st.markdown("### Loi de Poisson")
            st.latex(r"P(X=k) = \frac{\lambda^k e^{-\lambda}}{k!}")
            st.write("**Usage :** Standard pour la fréquence des sinistres (rares et indépendants).")
            lam = st.slider("Lambda (λ)", 0.1, 20.0, 5.0, 0.1)
            mu = lam
            var = lam
            
        x = np.arange(0, int(lam * 3) + 5)
        pmf = poisson.pmf(x, lam)
        
    elif dist_type == "Binomiale Négative":
        with col_param:
            st.markdown("### Loi Binomiale Négative")
            st.write("**Usage :** Fréquence avec sur-dispersion (Variance > Moyenne).")
            n = st.slider("Nombre de succès (n)", 1, 50, 5)
            p = st.slider("Probabilité de succès (p)", 0.1, 0.9, 0.5)
            mu = n * (1-p) / p
            var = n * (1-p) / p**2
            
        x = np.arange(0, int(mu * 3) + 5)
        pmf = nbinom.pmf(x, n, p)

    elif dist_type == "Binomiale":
        with col_param:
            st.markdown("### Loi Binomiale")
            st.latex(r"P(X=k) = \binom{n}{k} p^k (1-p)^{n-k}")
            st.write("**Usage :** Nombre de décès dans un portefeuille, Rétention (Bernoulli répété).")
            n_b = st.slider("Nombre d'essais (n)", 1, 100, 20)
            p_b = st.slider("Probabilité (p)", 0.0, 1.0, 0.5)
            mu = n_b * p_b
            var = n_b * p_b * (1 - p_b)
            
        x = np.arange(0, n_b + 1)
        pmf = binom.pmf(x, n_b, p_b)

    with col_viz:
        fig = go.Figure()
        fig.add_trace(go.Bar(x=x, y=pmf, name=dist_type))
        fig.update_layout(title=f"Distribution de Masse de Probabilité (PMF) - {dist_type}", xaxis_title="k", yaxis_title="P(X=k)")
        st.plotly_chart(fig, use_container_width=True)
        
        st.info(f"**Moments :** Espérance = {mu:.2f} | Variance = {var:.2f} | Ratio V/E = {var/mu:.2f}")

with tab_continuous:
    st.header("Modélisation de la Sévérité (Coûts)")
    
    dist_cont = st.selectbox("Choisir une loi", ["Normale", "Lognormale", "Gamma", "Pareto"])
    
    col_param_c, col_viz_c = st.columns([1, 2])
    
    x_c = np.linspace(0, 100, 1000)
    
    if dist_cont == "Normale":
        with col_param_c:
            st.markdown("### Loi Normale")
            st.latex(r"f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{1}{2}(\frac{x-\mu}{\sigma})^2}")
            st.write("**Usage :** Théorème Central Limite, agrégation de risques, rendements d'actifs (log-returns).")
            mu_n = st.slider("Moyenne (μ)", -50.0, 50.0, 0.0)
            sigma_n = st.slider("Ecart-type (σ)", 0.1, 20.0, 1.0)
            
        x_c = np.linspace(mu_n - 4*sigma_n, mu_n + 4*sigma_n, 1000)
        pdf = norm.pdf(x_c, mu_n, sigma_n)
        
    elif dist_cont == "Lognormale":
        with col_param_c:
            st.markdown("### Loi Lognormale")
            st.write("**Usage :** Coût des sinistres (asymétrie positive), prix des actifs (Black-Scholes).")
            s = st.slider("Sigma (shape)", 0.1, 2.0, 0.5)
            scale = st.slider("Scale (exp(mu))", 1.0, 50.0, 10.0)
            
        pdf = lognorm.pdf(x_c, s, scale=scale)
        
    elif dist_cont == "Gamma":
        with col_param_c:
            st.markdown("### Loi Gamma")
            st.write("**Usage :** Coût moyen des sinistres (GLM), temps d'attente.")
            a = st.slider("Alpha (Shape)", 0.1, 10.0, 2.0)
            scale_g = st.slider("Theta (Scale)", 0.1, 20.0, 5.0)
            
        pdf = gamma.pdf(x_c, a, scale=scale_g)
        
    elif dist_cont == "Pareto":
        with col_param_c:
            st.markdown("### Loi de Pareto")
            st.latex(r"f(x) = \frac{\alpha x_m^\alpha}{x^{\alpha+1}}")
            st.write("**Usage :** Grands sinistres (Queues épaisses), Réassurance XL.")
            b = st.slider("Alpha (Shape)", 1.0, 10.0, 3.0)
            loc = st.slider("Xm (Scale/Location)", 1.0, 50.0, 10.0)
            
        x_c = np.linspace(loc, loc + 100, 1000)
        pdf = pareto.pdf(x_c, b, scale=loc)

    with col_viz_c:
        fig_c = go.Figure()
        fig_c.add_trace(go.Scatter(x=x_c, y=pdf, mode='lines', fill='tozeroy', name=dist_cont))
        fig_c.update_layout(title=f"Densité de Probabilité (PDF) - {dist_cont}", xaxis_title="x", yaxis_title="f(x)")
        st.plotly_chart(fig_c, use_container_width=True)

st.divider()
st.header("Synthèse des usages")
st.table(pd.DataFrame({
    "Loi": ["Poisson", "Binomiale Négative", "Gamma", "Lognormale", "Pareto", "Normale"],
    "Type": ["Discrète", "Discrète", "Continue", "Continue", "Continue", "Continue"],
    "Application Actuarielle Principale": [
        "Fréquence des sinistres de masse (Auto, MRH)",
        "Fréquence avec forte variabilité (Cat Nat, RC Pro)",
        "Coût des sinistres attritifs (GLM)",
        "Coût des sinistres moyens à graves, Actifs financiers",
        "Sinistres extrêmes (Queues lourdes), Réassurance",
        "Approximation (TCL), VaR paramétrique"
    ]
}))