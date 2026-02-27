import streamlit as st
import chainladder as cl
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration de la page
st.set_page_config(page_title="Capital Simulator - Solvency II", layout="wide")

st.title("🛡️ Simulateur de Capital Économique (Bootstrap & SII)")
st.markdown("""
Cette application simule la variabilité des provisions techniques pour calculer le **SCR (Solvency Capital Requirement)** en utilisant une approche stochastique (Bootstrap).
""")

# --- 1. CHARGEMENT ET PRÉPARATION DES DONNÉES ---
# Utilisation du dataset 'genins' (General Insurance) souvent utilisé pour les démos de provisionnement
@st.cache_data
def load_data():
    data = cl.load_dataset('genins')
    return data

data = load_data()
triangle = cl.Triangle(data, origin='origin', development='development', columns='incremental')

# --- 2. CONFIGURATION DU MODÈLE (Main Panel) ---
with st.expander("⚙️ Paramètres de la Simulation", expanded=True):
    col_param1, col_param2, col_param3 = st.columns(3)
    with col_param1:
        n_sim = st.number_input("Nombre de simulations Bootstrap", min_value=100, max_value=10000, value=1000, step=100)
    with col_param2:
        confidence_level = st.slider("Niveau de confiance (VaR %)", 90.0, 99.9, 99.5, step=0.1)
    with col_param3:
        tail_factor = st.number_input("Facteur de queue (Tail Factor)", min_value=1.0, max_value=2.0, value=1.0, step=0.01)

# --- 3. CALCULS ACTUARIELS ---
# Calcul Mack pour la Best Estimate déterministe
mack = cl.MackChainladder().fit(triangle)
if tail_factor > 1.0:
    # Ajustement manuel du facteur de queue si spécifié
    mack.tail_ = tail_factor

# Modèle Bootstrap
with st.spinner('Exécution des simulations stochastiques...'):
    bootstrap = cl.BootstrapModel(n_sim=n_sim, random_state=42)
    bootstrap.fit(triangle)
    
    # Distribution des réserves totales (somme sur toutes les années de survenance)
    # On accède à la distribution des réserves via l'attribut full_expectation_
    reserves_dist = bootstrap.full_expectation_.sum('development').sum('origin').to_frame()
    reserves_dist.columns = ['Total_Reserves']

# --- 4. AFFICHAGE DES INDICATEURS CLÉS (KPIs) ---
be_value = mack.full_expectation_.sum()
var_value = reserves_dist['Total_Reserves'].quantile(confidence_level / 100)
scr_value = max(0, var_value - be_value)

st.markdown("---")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Best Estimate (Mack)", f"{be_value:,.0f} €")
kpi2.metric(f"VaR {confidence_level}%", f"{var_value:,.0f} €")
kpi3.metric("SCR Provisionnement", f"{scr_value:,.0f} €", delta_color="inverse")
kpi4.metric("Ratio SCR/BE", f"{(scr_value/be_value)*100:.2f} %")

# --- 5. VISUALISATION ET ANALYSE DE SENSIBILITÉ ---
tab1, tab2 = st.tabs(["📊 Distribution du Capital", "🔍 Analyse de Sensibilité"])

with tab1:
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(reserves_dist['Total_Reserves'], kde=True, color="#2E86C1", ax=ax)
    ax.axvline(be_value, color='green', linestyle='--', label='Best Estimate')
    ax.axvline(var_value, color='red', linestyle='-', label=f'VaR {confidence_level}%')
    ax.set_title(f"Distribution stochastique des provisions (n={n_sim})")
    ax.set_xlabel("Provisions totales (€)")
    ax.legend()
    st.pyplot(fig)

with tab2:
    st.subheader("Sensibilité au Tail Factor (Facteur de queue)")
    st.info("Ici, nous pourrions itérer sur plusieurs facteurs de queue pour voir l'élasticité du SCR.")
    
    # Petit calcul rapide de sensibilité
    sensi_tail = [1.0, 1.05, 1.10, 1.15]
    results_sensi = []
    for t in sensi_tail:
        # Simulation simplifiée pour la démo
        impact = be_value * t
        results_sensi.append({"Tail Factor": t, "Nouvelle BE": impact, "Impact SCR (est.)": impact - be_value})
    
    st.table(pd.DataFrame(results_sensi))

# --- 6. EXPORT DES DONNÉES ---
st.download_button(
    label="Exporter les simulations (CSV)",
    data=reserves_dist.to_csv().encode('utf-8'),
    file_name='simulations_actuariat.csv',
    mime='text/csv',
)