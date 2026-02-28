import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Best Estimate Vie", layout="wide")

st.title("💰 Best Estimate Liabilities (BEL) - Vie")
st.subheader("Projection des Flux de Trésorerie (Cash Flows)")

st.markdown("""
Le **Best Estimate (BEL)** correspond à la valeur actuelle probable des flux de trésorerie futurs, pondérée par leur probabilité de survenance.
""")

st.latex(r"BEL = \sum_{t=1}^{T} \frac{E[Flux_{Sortants}(t)] - E[Flux_{Entrants}(t)]}{(1 + r_t)^t}")

st.markdown("""
Ce module simule la projection d'un portefeuille d'épargne standard (Fonds Euros) sur 60 ans.
Les **primes futures** sont projetées en déduction des engagements (Flux Entrants), sous réserve des frontières de contrat.
""")

st.divider()

# --- 1. HYPOTHÈSES DE MODÉLISATION ---
st.header("1. Hypothèses de Projection")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Portefeuille")
    encours_initial = st.number_input("Encours Initial (PM) (M€)", 100.0, 5000.0, 1000.0, step=100.0)
    prime_annuelle = st.number_input("Primes Futures Annuelles (M€)", 0.0, 200.0, 50.0, step=10.0)
    age_moyen = st.slider("Âge moyen du portefeuille", 20, 80, 45)

with col2:
    st.subheader("Comportement & Frais")
    taux_rachat = st.slider("Taux de Rachat Structurel (%)", 0.0, 15.0, 4.0, 0.5) / 100
    frais_gestion = st.slider("Frais de Gestion (% Encours)", 0.1, 2.0, 0.60, 0.05) / 100
    choc_mass_lapse = st.checkbox("Appliquer un Choc Rachat Massif (40% en t=1) ?", value=False)

with col3:
    st.subheader("Environnement Éco")
    taux_tech = st.number_input("Taux Revalorisation (PB) (%)", 0.0, 5.0, 2.0, 0.1) / 100
    taux_actualisation = st.slider("Taux d'Actualisation (Plat) (%)", 0.0, 6.0, 2.5, 0.1) / 100

st.caption("ℹ️ **Hypothèse de modélisation :** Les primes futures sont projetées sur une durée limitée de **20 ans** (phase d'épargne active), tandis que les prestations (décès, rachats) sont modélisées jusqu'à l'extinction du portefeuille (60 ans).")

# --- 2. MOTEUR DE CALCUL ---
horizon = 60
years = np.arange(1, horizon + 1)

# Loi de mortalité simplifiée (Gompertz-Makeham)
def get_qx(age):
    # qx augmente exponentiellement avec l'âge
    return np.minimum(1.0, 0.00005 * np.exp(0.095 * age))

# Initialisation des vecteurs
encours = np.zeros(horizon + 1)
encours[0] = encours_initial

flux_primes = np.zeros(horizon)
flux_rachats = np.zeros(horizon)
flux_deces = np.zeros(horizon)
flux_frais = np.zeros(horizon)

for t in range(horizon):
    age_actuel = age_moyen + t
    
    # 1. Flux Entrants (Primes)
    # Hypothèse : les primes cessent progressivement (ex: départ en retraite)
    flux_primes[t] = prime_annuelle * (0.90 ** t) if t < 20 else 0
    
    # 2. Base de calcul
    base_calcul = encours[t] + flux_primes[t]
    
    # 3. Flux Sortants (Prestations & Frais)
    qx = get_qx(age_actuel)
    rachat_t = 0.40 if (choc_mass_lapse and t == 0) else taux_rachat
    
    montant_deces = base_calcul * qx
    montant_rachats = base_calcul * rachat_t
    montant_frais = base_calcul * frais_gestion
    
    flux_deces[t] = montant_deces
    flux_rachats[t] = montant_rachats
    flux_frais[t] = montant_frais
    
    # 4. Revalorisation du stock restant (Capitalisation)
    stock_fin = (base_calcul - montant_deces - montant_rachats - montant_frais) * (1 + taux_tech)
    encours[t+1] = stock_fin

# Flux Net S2 = Sorties - Entrées
flux_net = (flux_deces + flux_rachats + flux_frais) - flux_primes

# Actualisation
discount_factors = 1 / ((1 + taux_actualisation) ** years)
flux_actualises = flux_net * discount_factors
bel = np.sum(flux_actualises)

# --- 3. RÉSULTATS & VISUALISATION ---
st.divider()
st.header("2. Résultats de la Projection")

col_res1, col_res2 = st.columns(2)
col_res1.metric("Best Estimate (BEL)", f"{bel:,.1f} M€", delta="Valeur Actuelle des Engagements")
col_res2.metric("Ratio BEL / Encours", f"{bel/encours_initial*100:.1f}%", help="Indicateur de valeur : < 100% signifie que le portefeuille génère de la valeur future (VIF).")

# Graphique des flux
fig = go.Figure()
fig.add_trace(go.Bar(x=years, y=-flux_primes, name="Primes (In)", marker_color='green'))
fig.add_trace(go.Bar(x=years, y=flux_deces, name="Décès (Out)", marker_color='red'))
fig.add_trace(go.Bar(x=years, y=flux_rachats, name="Rachats (Out)", marker_color='orange'))
fig.add_trace(go.Bar(x=years, y=flux_frais, name="Frais (Out)", marker_color='gray'))
fig.add_trace(go.Scatter(x=years, y=flux_net, name="Flux Net de Trésorerie", line=dict(color='black', width=3)))

fig.update_layout(title="Projection des Flux de Trésorerie (Non actualisés)", barmode='relative', xaxis_title="Année de projection", yaxis_title="Montant (M€)", height=500)
st.plotly_chart(fig, use_container_width=True)

st.info("💡 **Lecture :** Les barres vertes (négatives) représentent les entrées d'argent (Primes). Les barres positives (rouge/orange) sont les sorties. La ligne noire est le solde net à financer.")

with st.expander("🔎 Point Technique : Frontières de Contrat (Contract Boundaries)", expanded=True):
    st.markdown("""
    En Solvabilité II, on ne projette les primes futures que si elles rentrent dans la **Frontière du Contrat**.
    C'est-à-dire si l'assureur n'a pas le droit unilatéral de résilier le contrat, de refuser la prime ou de modifier les tarifs pour refléter le nouveau risque.
    """)

st.divider()

st.header("3. Structure de la Provision Technique")
st.markdown("""
Il est important de rappeler que le BEL n'est qu'une partie des provisions techniques (PT) sous Solvabilité II :

$$ PT = BEL + RiskMargin $$

La **Risk Margin (marge de risque)** vient s'ajouter pour couvrir l'incertitude liée aux risques non diversifiables, garantissant que les provisions correspondent au montant qu'un autre assureur demanderait pour reprendre les engagements.
""")

st.subheader("Formule de la Marge de Risque")
st.latex(r"RM = CoC \times \sum_{t \ge 0} \frac{SCR(t)}{(1 + r(t+1))^{t+1}}")
st.markdown("""
*   **CoC (Cost of Capital) :** Le coût du capital, fixé réglementairement à **6%**.
*   **SCR(t) :** Le Capital de Solvabilité Requis projeté à l'année $t$ (couvrant les risques non-couvrables).
*   **Actualisation :** Au taux sans risque $r$.
""")