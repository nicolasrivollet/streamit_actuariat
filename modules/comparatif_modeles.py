import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Comparatif Modèles de Taux", layout="wide")

st.title("🔬 Comparatif des Méthodologies de Modélisation")
st.markdown("""
Le choix d'un modèle de courbe des taux dépend de l'objectif visé : 
précision locale, stabilité économique ou conformité réglementaire.
""")

st.divider()

# --- SECTION 1 : LES TROIS FAMILLES ---
st.header("1. Les Familles de Modèles")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Paramétriques")
    st.write("**Philosophie :** Décrire la courbe par une fonction mathématique globale.")
    st.info("Exemples : Nelson-Siegel, Svensson.")
    st.markdown("- ✅ Interprétable\n- ✅ Lisse\n- ❌ Ne colle pas parfaitement au marché")

with col2:
    st.subheader("Interpolation / Splines")
    st.write("**Philosophie :** Relier les points de marché par des segments de polynômes.")
    st.info("Exemples : Splines Cubiques, B-Splines.")
    st.markdown("- ✅ Précision maximale\n- ✅ Zéro résidu\n- ❌ Risque d'instabilité (courbe nerveuse)")

with col3:
    st.subheader("Convergence (Hybrides)")
    st.write("**Philosophie :** Interpolation sur la partie liquide, puis extrapolation vers une cible.")
    st.info("Exemple : Smith-Wilson (EIOPA).")
    st.markdown("- ✅ Standard réglementaire\n- ✅ Extrapolation longue durée\n- ❌ Complexité de calcul")

st.divider()

# --- SECTION 2 : VISUALISATION COMPARATIVE ---
st.header("2. Illustration visuelle des approches")

# Simulation de données
t = np.linspace(0.1, 40, 200)
t_market = np.array([1, 2, 5, 10, 20])
y_market = np.array([0.025, 0.028, 0.032, 0.035, 0.038])

# Modèle Lisse (type Nelson-Siegel)
y_smooth = 0.04 - 0.02 * np.exp(-t/2)

# Modèle "Overfitted" (type Splines qui cherche les points)
y_spline = np.interp(t, t_market, y_market) 

fig = go.Figure()
fig.add_trace(go.Scatter(x=t, y=y_smooth*100, name="Approche Paramétrique (Lisse)", line=dict(dash='dash', color='blue')))
fig.add_trace(go.Scatter(x=t, y=y_spline*100, name="Approche Interpolation (Exacte)", line=dict(color='green')))
fig.add_trace(go.Scatter(x=t_market, y=y_market*100, name="Points de Marché", mode='markers', marker=dict(color='red', size=10)))

fig.update_layout(
    title="Lissage vs Fidélité au marché",
    xaxis_title="Maturité (Ans)",
    yaxis_title="Taux (%)",
    template="plotly_white",
    legend=dict(yanchor="bottom", y=0.01, xanchor="right", x=0.99)
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# --- SECTION 3 : TABLEAU SYNTHÉTIQUE ---
st.header("3. Matrice de Sélection")

data = {
    "Modèle": ["Nelson-Siegel", "Svensson", "Smith-Wilson", "Splines Cubiques", "Hull-White"],
    "Usage Type": ["Analyse ALM / Interne", "Banques Centrales", "S2 - Best Estimate", "Trading / Pricing", "Valorisation Options"],
    "Philosophie": ["Parcimonie", "Flexibilité", "Réglementaire", "Fidélité Marché", "Stochastique"],
    "Point Fort": ["Interprétabilité des facteurs", "Capture 2 bosses", "Extrapolation (UFR)", "Zéro erreur de fitting", "Gestion du temps"],
    "Point Faible": ["Manque de précision locale", "Calibration instable", "Boîte noire mathématique", "Instabilité des forwards", "Complexité mathématique"]
}

df = pd.DataFrame(data)
st.table(df)

st.divider()

# --- SECTION 4 : PERSPECTIVE ACTUARIELLE ---
st.header("4. L'avis de l'expert")
st.markdown("""
Le choix du modèle n'est pas neutre :
1. **Pour un inventaire Solvabilité II**, la question ne se pose pas : c'est **Smith-Wilson** car la comparabilité entre assureurs prime.
2. **Pour le pilotage de la stratégie d'investissement**, on préférera **Nelson-Siegel** car il permet de décomposer le risque en 'mouvements de niveau' ou 'mouvements de pente'.
3. **Pour du Hedging**, on utilisera les **Splines** pour s'assurer que l'instrument de couverture est valorisé exactement comme au marché.
""")

st.caption("Analyse comparative - Nicolas Rivollet | Portfolio Actuariat")