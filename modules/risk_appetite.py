import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Cadre d'Appétence au Risque", layout="wide")

st.title("🎯 Cadre d'Appétence au Risque (Risk Appetite Framework)")
st.subheader("Définir, Mesurer et Piloter la prise de risque")

st.markdown("""
L'**Appétence au Risque** est le niveau de risque agrégé qu'un assureur est prêt à accepter pour atteindre ses objectifs stratégiques.
Ce cadre (RAF) est la boussole du pilotage : il traduit la stratégie en limites opérationnelles concrètes pour chaque nature de risque.
""")

st.divider()

# --- 1. LA PYRAMIDE DU RAF ---
st.header("1. La Pyramide du RAF")
st.markdown("Le cadre se décline en trois niveaux de granularité :")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("### 1. Risk Appetite\n**La Cible (Target)**")
    st.write("Le niveau de risque souhaité pour créer de la valeur.")
    st.caption("Ex: 'Nous visons un ratio de solvabilité de 200%'.")

with col2:
    st.warning("### 2. Risk Tolerance\n**La Zone de Tolérance**")
    st.write("La variabilité acceptée autour de la cible avant action corrective.")
    st.caption("Ex: 'Le ratio peut fluctuer entre 180% et 220%'.")

with col3:
    st.error("### 3. Risk Limits\n**La Limite (Hard Limit)**")
    st.write("Le seuil infranchissable qui déclenche une crise ou un plan de rétablissement.")
    st.caption("Ex: 'Interdiction absolue de descendre sous 150%'.")

st.divider()

# --- 2. TABLEAU DE BORD (COCKPIT) ---
st.header("2. Cockpit des Indicateurs Clés (KRI)")
st.markdown("Simulez la position actuelle de la compagnie pour visualiser le statut des indicateurs par rapport aux seuils définis.")

# KRI 1 : Solvabilité
st.subheader("🛡️ Solvabilité (Ratio S2)")
col_s1, col_s2 = st.columns([1, 2])

with col_s1:
    s2_ratio = st.slider("Ratio de Solvabilité Actuel (%)", 100, 250, 190, step=5)
    
    # Seuils
    limit_s2 = 140
    tolerance_low_s2 = 170
    target_s2 = 200
    
    if s2_ratio < limit_s2:
        st.error("🔴 **Statut : BREACH (Crise)**\n\nDéclenchement du Plan de Rétablissement.")
    elif s2_ratio < tolerance_low_s2:
        st.warning("🟠 **Statut : TOLERANCE (Vigilance)**\n\nInformation du Conseil et mesures correctives.")
    else:
        st.success("🟢 **Statut : CONFORT**\n\nSituation conforme à l'appétence.")

with col_s2:
    fig_s2 = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = s2_ratio,
        delta = {'reference': target_s2, 'position': "top"},
        title = {'text': "Ratio S2"},
        gauge = {
            'axis': {'range': [100, 250]},
            'bar': {'color': "black"},
            'steps': [
                {'range': [100, limit_s2], 'color': "#ef5350"}, # Red
                {'range': [limit_s2, tolerance_low_s2], 'color': "#ffca28"}, # Orange
                {'range': [tolerance_low_s2, 250], 'color': "#66bb6a"} # Green
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': limit_s2}
        }
    ))
    fig_s2.update_layout(height=250, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_s2, use_container_width=True)

# KRI 2 : Liquidité & Rentabilité
col_kri1, col_kri2 = st.columns(2)

with col_kri1:
    st.subheader("💧 Liquidité")
    liq_ratio = st.slider("Ratio Actifs Liquides / Passifs Exigibles (%)", 0, 100, 45, step=5)
    limit_liq = 20
    target_liq = 40
    
    delta_col = "normal" if liq_ratio >= target_liq else "inverse"
    st.metric("Ratio de Liquidité", f"{liq_ratio}%", delta=f"{liq_ratio - target_liq} pts vs Cible", delta_color=delta_col)
    
    if liq_ratio < limit_liq:
        st.error(f"⚠️ Inférieur à la limite stricte ({limit_liq}%)")
    else:
        st.progress(min(liq_ratio / 100 * 1.5, 1.0)) # Scaling visuel

with col_kri2:
    st.subheader("💰 Rentabilité (ROE)")
    roe = st.slider("Return on Equity (%)", -5.0, 20.0, 8.0, 0.5)
    limit_roe = 5.0
    target_roe = 10.0
    
    delta_col = "normal" if roe >= target_roe else "inverse"
    st.metric("ROE", f"{roe}%", delta=f"{roe - target_roe:.1f} pts vs Cible", delta_color=delta_col)
    
    if roe < limit_roe:
        st.error(f"⚠️ Rentabilité insuffisante (< {limit_roe}%)")
    else:
        st.progress(min(max(0, roe) / 20, 1.0))

st.divider()

# --- 3. CARTOGRAPHIE DES RISQUES ---
st.header("3. Matrice de Matérialité (Heatmap)")
st.markdown("Positionnement des risques majeurs par rapport aux zones d'appétence.")

# Données fictives
data_risk = {
    'Risque': ['Marché (Actions)', 'Taux Bas', 'Cyber', 'Rachat Massif', 'Crédit', 'Climat', 'Opérationnel'],
    'Probabilité': [3.5, 4.0, 2.5, 1.5, 3.0, 4.5, 2.0], # 1-5
    'Impact': [4.0, 3.0, 4.5, 5.0, 2.5, 3.5, 2.0],       # 1-5
    'Catégorie': ['Financier', 'Financier', 'Opérationnel', 'Souscription', 'Financier', 'ESG', 'Opérationnel']
}
df_risk = pd.DataFrame(data_risk)

fig_map = px.scatter(df_risk, x="Probabilité", y="Impact", text="Risque", size=[40]*7, color="Catégorie",
                     range_x=[0.5, 5.5], range_y=[0.5, 5.5], template="plotly_white")

fig_map.update_traces(textposition='top center', marker=dict(line=dict(width=2, color='DarkSlateGrey')))

# Ajout des zones de couleur (Background)
fig_map.add_shape(type="rect", x0=3.5, y0=3.5, x1=5.5, y1=5.5, fillcolor="red", opacity=0.1, layer="below", line_width=0)
fig_map.add_shape(type="rect", x0=0.5, y0=0.5, x1=2.5, y1=2.5, fillcolor="green", opacity=0.1, layer="below", line_width=0)

fig_map.update_layout(
    title="Matrice Probabilité / Impact",
    xaxis_title="Probabilité (Fréquence)",
    yaxis_title="Impact Financier (Sévérité)",
    height=500
)
st.plotly_chart(fig_map, use_container_width=True)

st.info("💡 **Lecture :** Les risques situés dans la zone rouge (Haut/Droite) sont hors appétence et nécessitent des plans d'action (Mitigation).")