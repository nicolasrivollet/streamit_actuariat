import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Moteur IFRS 17 (CSM)", layout="wide")

st.title("📊 Moteur IFRS 17 : Modèle Général (GMM)")
st.subheader("Simulation de la Marge de Service Contractuelle (CSM)")

st.markdown("""
Sous IFRS 17, la **CSM (Contractual Service Margin)** représente le profit non gagné que l'entité comptabilisera au fur et à mesure qu'elle fournira les services d'assurance.
Ce module simule la comptabilisation initiale et l'amortissement de la CSM pour un groupe de contrats.
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
st.markdown("La CSM s'amortit en fonction des **Unités de Couverture (Coverage Units)** fournies sur la période.")

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
    
    curr_csm = csm_initial
    
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

    # DataFrame résultats
    df_proj = pd.DataFrame({
        "Année": years,
        "CSM Début": csm_balance[:-1],
        "Intérêts (Accrétion)": csm_interest,
        "Libération (P&L)": csm_release,
        "CSM Fin": csm_balance[1:]
    })
    
    st.dataframe(df_proj.style.format("{:.1f}"))

# Graphique Amortissement
fig_proj = go.Figure()
fig_proj.add_trace(go.Bar(x=years, y=df_proj["Libération (P&L)"], name="Revenu CSM (P&L)", marker_color='green'))
fig_proj.add_trace(go.Scatter(x=years, y=df_proj["CSM Fin"], name="Stock CSM (Bilan)", line=dict(color='blue', width=3)))

fig_proj.update_layout(title="Projection de la CSM : Stock vs Flux", xaxis_title="Année", yaxis_title="Montant (€)")
st.plotly_chart(fig_proj, use_container_width=True)

st.info("""
**Mécanique IFRS 17 :**
1.  **Accrétion :** La CSM grossit avec le temps (valeur temps de l'argent) au taux locked-in.
2.  **Libération :** Une part est reconnue en résultat (Revenu d'Assurance) proportionnellement au service rendu (Coverage Units).
""")