import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Modèle Smith-Wilson", layout="wide")

# --- HEADER ---
st.title("📏 Modélisation Smith-Wilson")
st.subheader("Standard Prudentiel Solvabilité II (EIOPA)")

st.markdown("""
Le modèle Smith-Wilson est utilisé pour extrapoler la courbe des taux au-delà des données de marché liquides. 
Contrairement aux modèles paramétriques, il garantit une interpolation parfaite des points observés tout en assurant 
une convergence lisse vers un taux cible de long terme.
""")

st.divider()

# --- INPUTS & PARAMETRAGE ---
st.header("1. Paramètres d'Extrapolation")

col_params, col_desc = st.columns([1, 2])

with col_params:
    ufr = st.slider("Ultimate Forward Rate (UFR) %", 2.0, 5.0, 3.45, step=0.05)
    llp = st.slider("Last Liquid Point (LLP) - Années", 10, 30, 20)
    alpha = st.slider("Paramètre de Convergence (Alpha)", 0.05, 0.50, 0.15, step=0.01)

with col_desc:
    st.markdown(f"""
    * **UFR ({ufr}%)** : Le taux vers lequel la courbe doit converger à l'infini. Il reflète les anticipations de croissance et d'inflation de long terme.
    * **LLP ({llp} ans)** : La maturité maximale où le marché est considéré comme profond et liquide.
    * **Alpha ({alpha})** : Détermine la vitesse à laquelle la courbe rejoint l'UFR après le LLP. Un alpha élevé signifie une convergence rapide.
    """)

# --- SIMULATION VISUELLE ---
# Génération d'une courbe simplifiée pour illustrer le concept (Interpolation + Extrapolation)
t = np.linspace(0.1, 60, 200)

# Fonction de simulation Smith-Wilson (logique simplifiée pour visualisation)
def simulate_sw(t, llp, ufr_val, alpha_val):
    ufr_decimal = ufr_val / 100
    # Partie liquide (jusqu'au LLP) : simule une montée de taux
    liquid_part = 0.04 - 0.02 * np.exp(-t/5)
    # Partie extrapolation (après LLP) : convergence vers UFR
    weight = np.exp(-alpha_val * np.maximum(0, t - llp))
    return weight * liquid_part + (1 - weight) * ufr_decimal

y_sw = simulate_sw(t, llp, ufr, alpha)

# --- GRAPHIQUE ---
fig = go.Figure()

# Zone Liquide vs Extrapolée
fig.add_vrect(x0=0, x1=llp, fillcolor="green", opacity=0.1, layer="below", line_width=0, annotation_text="Zone Liquide (Marché)")
fig.add_vrect(x0=llp, x1=60, fillcolor="blue", opacity=0.1, layer="below", line_width=0, annotation_text="Zone d'Extrapolation")

fig.add_trace(go.Scatter(x=t, y=y_sw*100, name="Courbe Smith-Wilson", line=dict(color='#2E86C1', width=4)))
fig.add_hline(y=ufr, line_dash="dash", line_color="red", annotation_text="Cible UFR")

fig.update_layout(
    title="Convergence de la Courbe vers l'UFR",
    xaxis_title="Maturité (Années)",
    yaxis_title="Taux (%)",
    template="plotly_white",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# --- LOGIQUE TECHNIQUE ---
st.header("2. Mécanisme de calcul")

tab1, tab2 = st.tabs(["L'algorithme", "L'importance des Forwards"])

with tab1:
    st.markdown("""
    L'algorithme se décompose en trois étapes :
    1. **Sourcing** : Récupération des taux zéro-coupon jusqu'au LLP (ex: Swaps 20 ans).
    2. **Système Matriciel** : Résolution d'un système pour trouver les coefficients qui permettent de passer par chaque point de marché.
    3. **Extrapolation** : Utilisation de la fonction de noyau de Wilson pour projeter les taux au-delà du LLP.
    """)
    st.latex(r"W(t, u) = e^{-UFR(t+u)} \left( \alpha \min(t,u) - \frac{1 - e^{-\alpha \max(t,u)}}{2} e^{-\alpha |t-u|} \right)")

with tab2:
    st.write("""
    Le véritable test de robustesse d'un modèle Smith-Wilson ne se voit pas sur les taux **Spot** (courbe bleue ci-dessus), 
    mais sur les taux **Forward**. 
    
    Une mauvaise calibration de l'Alpha peut entraîner des taux forwards aberrants juste après le LLP, 
    ce qui fausserait la valorisation des produits de couverture ou des options de rachat.
    """)



st.info("💡 **Conformité S2** : Pour les assureurs européens, cette courbe est fournie mensuellement par l'EIOPA. L'enjeu pour l'actuaire n'est pas de la recréer, mais de comprendre sa sensibilité aux changements de paramètres réglementaires.")