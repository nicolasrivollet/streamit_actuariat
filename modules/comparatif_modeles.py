import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.optimize import minimize
from scipy.interpolate import CubicSpline

st.set_page_config(page_title="Expertise Modèles de Taux", layout="wide")

st.title("Analyse des Méthodologies de Courbe")
st.markdown("""
En actuariat, la courbe des taux n'est pas qu'une simple ligne ; c'est le socle de la valorisation du bilan. 
Chaque modèle repose sur une hypothèse différente concernant la structure du marché.
""")

st.divider()

# --- MODÈLE 1 : NELSON-SIEGEL ---
with st.expander("1. Modèles Paramétriques : L'approche Nelson-Siegel & Svensson", expanded=True):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("""
        **Concept :** Ces modèles utilisent une fonction mathématique continue pour lisser l'ensemble de la courbe. 
        Le modèle **Nelson-Siegel** décompose le taux en trois composantes économiques :
        * **Le Niveau (Long Terme) :** Une constante $\\beta_0$.
        * **La Pente (Court Terme) :** Une fonction décroissante liée à $\\beta_1$.
        * **La Courbure (Moyen Terme) :** Une fonction en forme de bosse liée à $\\beta_2$.
        
        **L'extension de Svensson** ajoute un quatrième terme (deuxième courbure) pour capturer les anomalies ou les politiques monétaires complexes.
        """)
        st.success("**Usage idéal :** Pilotage ALM, Stress-testing interne, Analyse de scénarios économiques.")
    with col2:
        st.latex(r"y(t) = \beta_0 + \beta_1 f_1(t) + \beta_2 f_2(t)")
        st.warning("**Point de vigilance :** Ce modèle peut présenter des 'erreurs de fitting' (résidus) sur certaines maturités car il privilégie le lissage à la précision ponctuelle.")

st.divider()

# --- MODÈLE 2 : SMITH-WILSON ---
with st.expander("2. Modèles de Convergence : L'approche Smith-Wilson (EIOPA)", expanded=True):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("""
        **Concept :** C'est le standard de **Solvabilité II**. Ce modèle est conçu pour résoudre le problème de l'absence de marché liquide pour les très longues maturités (au-delà de 20 ans).
        
        **Fonctionnement :**
        * **Partie Liquide :** Le modèle utilise des noyaux mathématiques pour passer *exactement* par les points de marché observés.
        * **Point d'Extrapolation (LLP) :** À partir du *Last Liquid Point*, la courbe commence à converger.
        * **Cible (UFR) :** La courbe rejoint de manière "lisse" le *Ultimate Forward Rate*, un taux théorique de long terme défini par le régulateur.
        """)
        st.success("**Usage idéal :** Calcul du Best Estimate (BEL), valorisation des provisions techniques Vie de longue durée.")
    with col2:
        st.write("**Paramètres clés :**")
        st.markdown("- **LLP :** 20 ans (Zone Euro)\n- **UFR :** ~3.30% (2026)\n- **Alpha :** Vitesse de convergence")



st.divider()

# --- MODÈLE 3 : SPLINES CUBIQUES ---
with st.expander("3. Interpolation Locale : Les Splines Cubiques", expanded=True):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("""
        **Concept :** Au lieu d'une seule formule globale, on divise la courbe en petits segments (entre chaque maturité de marché). Sur chaque segment, on ajuste un polynôme de degré 3.
        
        **Avantages :**
        * **Zéro erreur :** La courbe passe mathématiquement par tous les points.
        * **Flexibilité :** Capable de reproduire n'importe quelle forme de courbe, même les plus erratiques.
        """)
        st.success("**Usage idéal :** Trading, Arbitrage, Pricing de produits dérivés où chaque point de base compte.")
    with col2:
        st.error("**Risque majeur :** L'instabilité des taux 'Forward'. Entre deux points, la courbe peut avoir des oscillations non-économiques.")

st.divider()

# --- MODÈLE 4 : MODÈLES STOCHASTIQUES ---
with st.expander("4. Modèles Dynamiques : Hull-White & Vasicek", expanded=True):
    st.write("""
    **Concept :** Contrairement aux modèles précédents qui sont des "photos" à un instant T, ces modèles sont des "vidéos". Ils modélisent la diffusion du taux dans le temps.
    
    * **Retour à la moyenne (Mean Reversion) :** L'idée que si le taux s'écarte trop de sa moyenne historique, il finira par y revenir.
    * **Volatilité :** Intègre le risque de mouvement brusque des taux.
    """)
    st.success("**Usage idéal :** Calcul de la valeur Temps des options (TVOG), ESG (Economic Scenario Generators), simulations de trajectoires de taux pour l'ORSA.")



st.divider()

# --- SYNTHÈSE DES IMPACTS BILANTIELS ---
st.header("Synthèse de l'Impact Actuariel")
st.table(pd.DataFrame({
    "Critère": ["Précision Marché", "Interprétabilité", "Réglementation", "Stabilité"],
    "Nelson-Siegel": ["Moyenne", "Maximale", "Interne uniquement", "Élevée"],
    "Smith-Wilson": ["Élevée", "Faible (Boîte noire)", "Standard S2", "Moyenne"],
    "Splines": ["Parfaite", "Nulle", "Non recommandée", "Faible"]
}))

st.info("**Conseil du Risk Manager :** Pour un pilotage efficace, il est souvent recommandé de suivre Nelson-Siegel pour comprendre les tendances de fond, tout en produisant les chiffres officiels en Smith-Wilson.")

st.divider()

# --- SECTION 2 : VISUALISATION COMPARATIVE ---
st.header("2. Illustration visuelle des approches")

# Simulation de données
t = np.linspace(0.1, 40, 200)
t_market = np.array([1, 2, 5, 10, 20])
y_market = np.array([0.025, 0.028, 0.032, 0.035, 0.038])

# 1. Modèle Paramétrique (Nelson-Siegel calibré)
def ns_curve(t, params):
    b0, b1, b2, tau = params
    term1 = (1 - np.exp(-t/tau)) / (t/tau)
    term2 = term1 - np.exp(-t/tau)
    return b0 + b1*term1 + b2*term2

res = minimize(lambda p: np.sum((ns_curve(t_market, p) - y_market)**2), 
               [0.04, -0.01, 0.0, 2.0], method='Nelder-Mead')
y_smooth = ns_curve(t, res.x)

# 2. Modèle Interpolation (Splines Cubiques)
cs = CubicSpline(t_market, y_market, bc_type='natural')
y_spline = cs(t)

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