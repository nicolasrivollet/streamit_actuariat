import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import norm

st.set_page_config(page_title="Modèles Risque de Marché", layout="wide")

st.title("📉 Modèles de Risque de Marché (Trading Book)")
st.subheader("De Bâle II.5 à FRTB : VaR, SVaR, IRC, CRM")

st.markdown("""
Cette page détaille les mesures de risque de marché utilisées pour le calcul des exigences de fonds propres des banques pour leurs activités de marché (Trading Book).
Ces mesures ont été renforcées suite à la crise de 2008 (Bâle 2.5) et évoluent avec la **Fundamental Review of the Trading Book (FRTB)**.
""")

st.divider()

# --- 1. VaR & Stressed VaR ---
st.header("1. Value-at-Risk (VaR) & Stressed VaR (SVaR)")

col1, col2 = st.columns(2)

with col1:
    st.info("### 📊 Value-at-Risk (VaR)")
    st.markdown("""
    La perte maximale potentielle sur un horizon donné (ex: 10 jours) avec un niveau de confiance donné (ex: 99%).
    *   **Calibrage :** Sur les 12 derniers mois (période courante).
    *   **Limite :** Procyclique (la VaR est basse quand les marchés sont calmes).
    """)

with col2:
    st.warning("### ⚡ Stressed VaR (SVaR)")
    st.markdown("""
    Introduite par Bâle 2.5 pour corriger la procyclicité de la VaR.
    *   **Calibrage :** Sur une période de 12 mois de **stress financier significatif** (ex: 2008).
    *   **Objectif :** Assurer un niveau de capital plancher même en période calme.
    """)

# Visualisation Interactive
st.subheader("Simulation : VaR vs SVaR")

vol_current = st.slider("Volatilité Courante (VaR)", 5.0, 50.0, 15.0, 1.0) / 100
vol_stressed = st.slider("Volatilité Stressée (SVaR)", 5.0, 100.0, 40.0, 1.0) / 100
confidence = st.selectbox("Niveau de Confiance", [0.95, 0.99], index=1)
horizon_days = 10

# Calcul VaR Paramétrique (1M€ portfolio)
exposure = 1_000_000
z_score = norm.ppf(confidence)
var = exposure * vol_current * np.sqrt(horizon_days/252) * z_score
svar = exposure * vol_stressed * np.sqrt(horizon_days/252) * z_score

c1, c2 = st.columns(2)
c1.metric(f"VaR ({confidence:.0%}, 10j)", f"{var:,.0f} €")
c2.metric(f"SVaR ({confidence:.0%}, 10j)", f"{svar:,.0f} €", delta=f"Ratio SVaR/VaR : {svar/var:.1f}x", delta_color="inverse")

# Graphique Distributions
x = np.linspace(-exposure*0.2, exposure*0.2, 1000)
pdf_var = norm.pdf(x, 0, exposure * vol_current * np.sqrt(horizon_days/252))
pdf_svar = norm.pdf(x, 0, exposure * vol_stressed * np.sqrt(horizon_days/252))

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=pdf_var, name="Distribution Courante (VaR)", fill='tozeroy', line=dict(color='blue')))
fig.add_trace(go.Scatter(x=x, y=pdf_svar, name="Distribution Stressée (SVaR)", fill='tozeroy', line=dict(color='red'), opacity=0.5))
fig.add_vline(x=-var, line_dash="dash", line_color="blue", annotation_text="VaR")
fig.add_vline(x=-svar, line_dash="dash", line_color="red", annotation_text="SVaR")
fig.update_layout(title="Distributions des P&L (VaR vs SVaR)", xaxis_title="P&L (€)", yaxis_title="Densité")
st.plotly_chart(fig, use_container_width=True)

st.divider()

# --- 2. IRC (Incremental Risk Charge) ---
st.header("2. Incremental Risk Charge (IRC)")
st.markdown("""
L'IRC complète la VaR pour les produits de crédit (Obligations, CDS) du Trading Book.
Il capture deux risques majeurs sur un horizon de **1 an** à **99.9%** :
1.  **Risque de Défaut (Default Risk) :** Le saut au défaut (Jump-to-Default).
2.  **Risque de Migration (Migration Risk) :** La perte de valeur due à la dégradation de la note de crédit (ex: passage de A à BBB).
""")

# Simulation IRC (Modèle Merton simplifié)
st.subheader("Simulateur IRC (Modèle Factoriel de Merton)")

col_irc1, col_irc2 = st.columns(2)

with col_irc1:
    st.markdown("**Paramètres du Portefeuille**")
    pd_avg = st.slider("Probabilité de Défaut Moyenne (PD)", 0.1, 10.0, 1.0, 0.1) / 100
    correlation = st.slider("Corrélation des Actifs (rho)", 0.0, 100.0, 20.0, 5.0) / 100
    lgd = st.slider("Perte en cas de Défaut (LGD)", 0.0, 100.0, 60.0, 5.0) / 100
    n_sim_irc = 5000

with col_irc2:
    st.markdown("**Résultats**")
    # Simulation Vectorisée (Vasicek Single Factor Model pour la distribution des pertes)
    # L = N( (N^-1(PD) - sqrt(rho)*Z) / sqrt(1-rho) )
    # Z ~ N(0,1)
    
    np.random.seed(42)
    Z = np.random.normal(0, 1, n_sim_irc)
    
    # 1. Calcul du seuil de défaut (Inverse loi Normale : norm.ppf)
    # On transforme la PD moyenne en un seuil sur une loi N(0,1).
    # Si la valeur d'actif de l'entreprise tombe sous ce seuil, elle fait défaut.
    thresh = norm.ppf(pd_avg)
    
    # 2. Calcul de la PD Conditionnelle (Formule de Vasicek : norm.cdf)
    # On ajuste le seuil en fonction du facteur systémique Z (l'économie) et de la corrélation.
    cond_pd = norm.cdf((thresh - np.sqrt(correlation) * Z) / np.sqrt(1 - correlation))
    
    # Pertes du portefeuille (en % de l'exposition) = Cond_PD * LGD
    portfolio_losses = cond_pd * lgd
    
    irc_999 = np.percentile(portfolio_losses, 99.9)
    expected_loss = np.mean(portfolio_losses)
    
    st.metric("IRC (VaR 99.9% 1 an)", f"{irc_999*100:.2f}%", delta="Capital Requis")
    st.metric("Perte Attendue (EL)", f"{expected_loss*100:.2f}%")

# Graphique Distribution IRC
fig_irc = go.Figure()
fig_irc.add_trace(go.Histogram(x=portfolio_losses*100, nbinsx=50, name='Distribution des Pertes', histnorm='probability'))
fig_irc.add_vline(x=irc_999*100, line_dash="dash", line_color="red", annotation_text="IRC (99.9%)")
fig_irc.update_layout(title="Distribution des Pertes de Crédit (Modèle Vasicek)", xaxis_title="Perte (%)", yaxis_title="Probabilité")
st.plotly_chart(fig_irc, use_container_width=True)

st.info("Ce modèle montre comment la corrélation épaissit la queue de distribution (Fat Tail), augmentant drastiquement le capital requis pour les événements rares (99.9%).")

st.divider()

# --- 3. CRM (Comprehensive Risk Measure) ---
st.header("3. Comprehensive Risk Measure (CRM)")
st.markdown("""
Le CRM est une mesure spécifique pour le **Portefeuille de Trading de Corrélation (CTP)** (ex: Tranches de CDO).
Il doit capturer des risques complexes que l'IRC ne couvre pas assez bien pour ces produits structurés.
""")

col_crm1, col_crm2 = st.columns(2)

with col_crm1:
    st.error("### 🕸️ Risques Couverts")
    st.markdown("""
    *   **Risque de Corrélation :** Impact du changement de corrélation entre les actifs sous-jacents.
    *   **Risque de Base :** Différence entre le CDS de l'indice et les CDS des composants.
    *   **Risque de Recouvrement :** Volatilité du LGD.
    """)

with col_crm2:
    st.warning("### 🛡️ Le Plancher (Floor)")
    st.markdown(r"""
    Pour éviter une sous-estimation par les modèles internes, le régulateur impose un plancher.
    
    $$ CRM \ge 8\% \times \text{Charge Standard (Méthode Forfaitaire)} $$
    """)

# Visualisation conceptuelle : Impact de la corrélation sur les tranches
st.subheader("Illustration : Sensibilité à la Corrélation (Tranches CDO)")

corr_range = np.linspace(0, 1, 100)
# Modèle jouet pour l'illustration
el_equity = 1 - 0.8 * corr_range # Equity souffre moins si corrélation haute (tout ou rien)
el_senior = 0.2 * corr_range**2  # Senior souffre plus si corrélation haute

fig_crm = go.Figure()
fig_crm.add_trace(go.Scatter(x=corr_range, y=el_equity, name="Perte Attendue Tranche Equity (0-3%)", line=dict(color='red')))
fig_crm.add_trace(go.Scatter(x=corr_range, y=el_senior, name="Perte Attendue Tranche Senior (10-100%)", line=dict(color='green')))
fig_crm.update_layout(title="Impact de la Corrélation sur le Risque des Tranches (Conceptuel)", xaxis_title="Corrélation", yaxis_title="Niveau de Risque (Perte)")
st.plotly_chart(fig_crm, use_container_width=True)

st.divider()

# --- 4. FUTUR : FRTB ---
st.header("4. L'avenir : FRTB (Fundamental Review of the Trading Book)")
st.markdown("""
La réforme FRTB remplace ces mesures par une approche plus cohérente.
""")
with st.expander("🔬 De la VaR à l'Expected Shortfall (ES)", expanded=True):
    st.markdown("""
    FRTB remplace la VaR par l'**Expected Shortfall (ES)** pour les modèles internes.
    *   **VaR :** "Quelle est la perte maximale qui ne sera pas dépassée avec X% de confiance ?" (un point sur la distribution).
    *   **ES :** "SI la perte dépasse le seuil de la VaR, quelle est sa valeur moyenne ?" (la moyenne de la queue de distribution).
    
    L'ES est donc plus sensible aux événements extrêmes (Fat Tails).
    """)
    
    es_vol = st.slider("Volatilité du P&L (%)", 1.0, 30.0, 10.0, 1.0, key="es_vol") / 100
    es_conf = 0.975 # Standard FRTB
    
    # Calculs
    pnl_stdev = 1_000_000 * es_vol
    alpha = 1 - es_conf
    
    var_975 = -norm.ppf(alpha) * pnl_stdev
    es_975 = pnl_stdev * norm.pdf(norm.ppf(alpha)) / alpha
    
    # Graphique
    x_es = np.linspace(-5 * pnl_stdev, 5 * pnl_stdev, 1000)
    pdf_es = norm.pdf(x_es, 0, pnl_stdev)
    
    fig_es = go.Figure()
    fig_es.add_trace(go.Scatter(x=x_es, y=pdf_es, name="Distribution P&L", line=dict(color='blue')))
    
    # Zone de la queue
    tail_x = np.linspace(-5 * pnl_stdev, -var_975, 100)
    tail_y = norm.pdf(tail_x, 0, pnl_stdev)
    fig_es.add_trace(go.Scatter(x=np.concatenate([tail_x, tail_x[::-1]]), y=np.concatenate([tail_y, np.zeros(len(tail_y))]), 
                                fill='toself', fillcolor='rgba(255,0,0,0.3)', line=dict(width=0), name=f'Queue ({alpha*100:.1f}%)'))

    fig_es.add_vline(x=-var_975, line_dash="dash", line_color="red", annotation_text=f"VaR {es_conf*100:.1f}%")
    fig_es.add_vline(x=-es_975, line_dash="dash", line_color="purple", annotation_text=f"ES {es_conf*100:.1f}%")
    
    fig_es.update_layout(title="Comparaison VaR vs. Expected Shortfall", xaxis_title="P&L (€)", yaxis_title="Densité")
    st.plotly_chart(fig_es, use_container_width=True)
    
    st.metric("Expected Shortfall (ES)", f"{es_975:,.0f} €", delta=f"{(es_975/var_975 - 1)*100:.1f}% plus élevé que la VaR", delta_color="inverse")

with st.expander("🧱 Du IRC/CRM au Default Risk Charge (DRC)", expanded=True):
    st.markdown("""
    Le **DRC** remplace l'IRC et le CRM. Il couvre le risque de saut au défaut (Jump-to-Default) pour toutes les positions sensibles au crédit (y compris les actions).
    
    *   **Horizon :** 1 an.
    *   **Confiance :** 99.9%.
    *   **Méthodologie :** VaR sur la distribution des pertes de défaut. Pas de diversification avec les autres risques de marché.
    """)
    
    st.subheader("Simulateur DRC (Simplifié)")
    
    col_drc1, col_drc2 = st.columns(2)

    with col_drc1:
        drc_exp_bonds = st.slider("Exposition Obligations (M€)", 0, 1000, 500, key="drc_bonds") * 1e6
        drc_exp_equity = st.slider("Exposition Actions (M€)", 0, 1000, 200, key="drc_equity") * 1e6
        drc_pd = st.slider("PD moyenne", 0.1, 5.0, 2.0, 0.1, key="drc_pd") / 100
        drc_corr = st.slider("Corrélation", 0.0, 100.0, 30.0, 5.0, key="drc_corr") / 100
    
    with col_drc2:
        # Hypothèses LGD
        lgd_bonds = 0.50
        lgd_equity = 1.00
        
        # Simulation
        Z_drc = np.random.normal(0, 1, 10000)
        thresh_drc = norm.ppf(drc_pd)
        cond_pd_drc = norm.cdf((thresh_drc - np.sqrt(drc_corr) * Z_drc) / np.sqrt(1 - drc_corr))
        
        losses_bonds = drc_exp_bonds * lgd_bonds * cond_pd_drc
        losses_equity = drc_exp_equity * lgd_equity * cond_pd_drc
        total_losses_drc = losses_bonds + losses_equity
        
        drc_value = np.percentile(total_losses_drc, 99.9)
        
        st.metric("Default Risk Charge (DRC)", f"{drc_value/1e6:,.1f} M€", help="VaR 99.9% des pertes de défaut sur 1 an.")
        
        fig_drc = go.Figure(go.Histogram(x=total_losses_drc/1e6, nbinsx=50, name='Distribution des Pertes', histnorm='probability'))
        fig_drc.add_vline(x=drc_value/1e6, line_dash="dash", line_color="red", annotation_text="DRC (99.9%)")
        fig_drc.update_layout(title="Distribution des Pertes de Défaut (DRC)", xaxis_title="Perte (M€)", yaxis_title="Probabilité")
        st.plotly_chart(fig_drc, use_container_width=True)