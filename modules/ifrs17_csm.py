import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Moteur IFRS 17 (CSM)", layout="wide")

st.title("Moteur IFRS 17 : Modèle Général (GMM)")
st.subheader("Simulation de la Marge de Service Contractuelle (CSM)")

st.markdown("""
### Comprendre la philosophie IFRS 17
La norme IFRS 17 (entrée en vigueur en 2023) révolutionne la comptabilité des assurances en passant d'une logique de "Primes encaissées" à une logique de **"Service rendu"**.

Le **Modèle Général (GMM)**, aussi appelé BBA (*Building Block Approach*), repose sur l'agrégation de 4 blocs pour valoriser le passif :
1.  **Flux de trésorerie futurs (BEL)** : La meilleure estimation des entrées (primes) et sorties (sinistres, frais).
2.  **Ajustement pour Risque (RA)** : Une marge pour couvrir l'incertitude des flux non-financiers.
3.  **Actualisation** : Prise en compte de la valeur temps de l'argent.
4.  **Marge de Service Contractuelle (CSM)** : Le profit non gagné, stocké au bilan et libéré au rythme du service.
""")

st.divider()

# --- 1. RECONNAISSANCE INITIALE ---
st.header("1. Reconnaissance Initiale (t=0)")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Flux de Trésorerie (Best Estimate)")
    pv_premiums = st.number_input("Valeur Actuelle des Primes (PV Inflows)", value=1000.0, step=50.0)
    pv_claims = st.number_input("Valeur Actuelle des Sinistres & Frais (PV Outflows)", value=800.0, step=50.0)
    risk_adjustment = st.number_input("Ajustement pour Risque (RA)", value=50.0, step=10.0, help="Compensation pour l'incertitude des flux non financiers.")

with col2:
    st.subheader("Calcul de la CSM Initiale")
    st.markdown("""
    **Principe du "No Gain at Inception" :**
    *   Si le contrat est **profitable**, le gain est mis en réserve dans la **CSM** (pas de profit immédiat).
    *   Si le contrat est **déficitaire**, la perte est reconnue **immédiatement** (Loss Component).
    """)
    
    # FCF = PV Outflows + RA - PV Inflows
    fcf = pv_claims + risk_adjustment - pv_premiums
    
    if fcf < 0:
        csm_initial = -fcf
        loss_component = 0.0
        st.success(f"✅ **Contrat Profitable**")
        st.metric("CSM Initiale", f"{csm_initial:.1f} €", help="Profit différé à amortir.")
    else:
        csm_initial = 0.0
        loss_component = fcf
        st.error(f"❌ **Contrat Onéreux (Onerous)**")
        st.metric("Composante Perte (P&L immédiat)", f"{loss_component:.1f} €", help="Perte comptabilisée immédiatement en résultat.")

# Visualisation Waterfall Initiale
fig_init = go.Figure(go.Waterfall(
    orientation = "v",
    measure = ["relative", "relative", "relative", "total"],
    x = ["Primes (In)", "Sinistres (Out)", "Risk Adj (RA)", "Marge (CSM)"],
    textposition = "outside",
    text = [f"+{pv_premiums}", f"-{pv_claims}", f"-{risk_adjustment}", f"{csm_initial}"],
    y = [pv_premiums, -pv_claims, -risk_adjustment, csm_initial],
    connector = {"line":{"color":"rgb(63, 63, 63)"}},
))
fig_init.update_layout(title="Construction du Passif IFRS 17 (BBA)", height=400)
st.plotly_chart(fig_init, use_container_width=True)

st.divider()

# --- 2. SUIVI ULTÉRIEUR (AMORTISSEMENT) ---
st.header("2. Suivi Ultérieur : Projection de la CSM")
st.markdown("""
La CSM est un "réservoir de profit" vivant. Elle évolue selon trois mécanismes :
1.  **Accrétion d'intérêts :** La CSM grossit avec le temps (désactualisation) au taux fixé à l'origine (*Locked-in rate*).
2.  **Ajustements (Unlock) :** Elle absorbe les changements d'hypothèses futures (ex: baisse de mortalité) pour lisser le résultat.
3.  **Libération (Amortissement) :** Une part est transférée en P&L en fonction des **Unités de Couverture (Coverage Units)**.
""")

col_proj1, col_proj2 = st.columns(2)

with col_proj1:
    duration = st.slider("Durée du contrat (années)", 1, 20, 10)
    interest_rate = st.slider("Taux d'accrétion (Locked-in Rate) %", 0.0, 10.0, 2.0, 0.5) / 100
    
    # Profil d'amortissement
    amort_profile = st.selectbox("Profil d'amortissement (Coverage Units)", ["Linéaire", "Dégressif (Sinistres)", "Progressif (Capital)"])

with col_proj2:
    # Génération des Coverage Units (CU)
    years = np.arange(1, duration + 1)
    if amort_profile == "Linéaire":
        cu = np.ones(duration)
    elif amort_profile == "Dégressif (Sinistres)":
        cu = np.linspace(10, 1, duration)
    else:
        cu = np.linspace(1, 10, duration)
    
    # Normalisation pour calcul des poids
    # Attention : Le calcul IFRS 17 se fait période par période.
    # Allocation ratio = CU_current / (CU_current + CU_future)
    
    # Simulation
    csm_balance = [csm_initial]
    csm_release = []
    csm_interest = []
    ra_balance = [risk_adjustment]
    ra_release_list = []
    
    curr_csm = csm_initial
    curr_ra = risk_adjustment
    
    for t in range(duration):
        # 1. Accrétion d'intérêts
        interest = curr_csm * interest_rate
        csm_interest.append(interest)
        curr_csm += interest
        
        # 2. Libération (Release)
        # Poids de l'année t par rapport au total restant (t à fin)
        cu_curr = cu[t]
        cu_future = np.sum(cu[t+1:]) if t < duration - 1 else 0
        
        release_ratio = cu_curr / (cu_curr + cu_future)
        release = curr_csm * release_ratio
        
        csm_release.append(release)
        curr_csm -= release
        csm_balance.append(curr_csm)
        
        # RA Release (Simplification : suit le même profil que la CSM pour l'exemple)
        ra_rel = curr_ra * release_ratio
        ra_release_list.append(ra_rel)
        curr_ra -= ra_rel
        ra_balance.append(curr_ra)

    # DataFrame résultats
    df_proj = pd.DataFrame({
        "Année": years,
        "CSM Début": csm_balance[:-1],
        "Intérêts (Accrétion)": csm_interest,
        "Libération (P&L)": csm_release,
        "CSM Fin": csm_balance[1:],
        "Libération RA": ra_release_list
    })
    
    st.dataframe(df_proj.style.format("{:.1f}"))

# --- 3. IMPACT P&L ---
st.header("3. Formation du Résultat (P&L)")
st.markdown("""
Sous IFRS 17, la ligne "Primes Émises" disparaît du compte de résultat. Elle est remplacée par le **Revenu d'Assurance**.

$$ \\text{Revenu d'Assurance} = \\text{Sinistres Attendus} + \\text{Libération du RA} + \\text{Libération de la CSM} $$
""")

# Graphique Amortissement
fig_proj = go.Figure()
fig_proj.add_trace(go.Bar(x=years, y=df_proj["Libération (P&L)"], name="Marge (CSM)", marker_color='green'))
fig_proj.add_trace(go.Bar(x=years, y=df_proj["Libération RA"], name="Risque (RA)", marker_color='orange'))
fig_proj.add_trace(go.Scatter(x=years, y=df_proj["CSM Fin"], name="Stock CSM Restant (Bilan)", line=dict(color='blue', width=3), yaxis='y2'))

fig_proj.update_layout(
    title="Contribution au Résultat (Revenu d'Assurance) & Stock Bilan",
    xaxis_title="Année", 
    yaxis=dict(title="Flux P&L (€)"),
    yaxis2=dict(title="Stock Bilan (€)", overlaying='y', side='right'),
    barmode='stack',
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
st.plotly_chart(fig_proj, use_container_width=True)

st.info("""
**Lecture du graphique :**
Les barres représentent le profit reconnu chaque année (Revenu). La ligne bleue représente le "réservoir" de profit futur qui diminue au fil du temps.
""")