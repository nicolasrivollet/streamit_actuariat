import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="SCR Luxembourg (Réassurance Intra-Groupe)", layout="wide")

st.title("🇱🇺 SCR Luxembourg : Modèle 100% Réassuré")
st.subheader("Impact de la Réassurance Intra-Groupe sur le Capital")

st.markdown("""
De nombreuses filiales luxembourgeoises de groupes français fonctionnent selon un modèle spécifique :
*   **Unit-Linked (UC) :** Le risque est porté par les assurés (sauf risque de frais).
*   **Fonds Général (Euro) :** Il est **réassuré à 100%** par la maison mère française (Quota Share).

**Conséquence :** Le risque de marché et de souscription sur le Fonds Général (Euro) disparaît du bilan de la filiale, mais il est remplacé par un **Risque de Contrepartie** massif envers la maison mère.
""")

st.divider()

# --- 1. PARAMÈTRES DU BILAN ---
st.header("1. Structure du Bilan")

col1, col2 = st.columns(2)

with col1:
    tp_euro = st.number_input("Provisions Techniques Fonds Général (M€)", value=500.0, step=50.0)
    tp_uc = st.number_input("Provisions Techniques Unités de Compte (M€)", value=1000.0, step=100.0)
    collecte_euro = st.number_input("Collecte Brute Fonds Général (M€)", value=50.0, step=10.0, help="Primes émises sur le fonds Euro (Impact SCR Opérationnel)")

with col2:
    rating_parent = st.selectbox("Rating Maison Mère (Réassureur)", ["AAA", "AA", "A", "BBB", "BB"], index=1)
    collateral = st.number_input("Collatéral (Nantissement) (M€)", value=0.0, step=50.0, help="Actifs déposés en garantie par le réassureur pour réduire le risque.")
    frais_uc = st.number_input("Frais de Gestion Annuels UC (M€)", value=10.0, step=1.0, help="Revenus de frais sur encours UC (Base du SCR Marché)")

# --- MOTEUR DE CALCUL ---
# A. SCR Marché
# Sur les UC, l'assureur ne porte pas le risque de marché, sauf sur ses frais futurs.
# Simplification : SCR Marché = Choc sur les revenus futurs (Frais de gestion)
# On suppose que le choc baisse la valeur actuelle des frais futurs de 20% (Mass Lapse / Baisse marchés).
scr_market = tp_uc * 0.005 * 0.20 * 10 # Proxy : Frais annuels * 20% choc * 10 ans duration

# B. SCR Vie
# Le risque de mortalité/longevité Euro est réassuré.
# Reste le risque de rachat massif sur les UC (perte de frais futurs) et le risque de dépenses.
scr_life = tp_uc * 0.005 * 0.40 * 5 # Proxy rachat massif

# C. SCR Contrepartie (Le gros morceau)
# Exposition = TP Euro - Collatéral
exposure = max(0, tp_euro - collateral)

# Probabilité de défaut (Facteurs S2 simplifiés)
# Charge estimée pour une concentration unique (Formule simplifiée pour l'illustration : ~3 * sqrt(PD))
charge_map = {"AAA": 0.015, "AA": 0.03, "A": 0.06, "BBB": 0.12, "BB": 0.25} 
scr_default = exposure * charge_map[rating_parent]

# D. SCR Opérationnel
# Formule Standard : Max(Primes, Provisions) pour le Fonds Général + 25% des frais pour les UC.
op_euro = max(tp_euro * 0.0045, collecte_euro * 0.04) # 0.45% des provisions ou 4% des primes
op_uc = frais_uc * 0.25 # 25% des frais annuels supportés par les UC
scr_op = op_euro + op_uc

# --- AGRÉGATION ---
# Matrice de corrélation simplifiée
# Marché et Vie sont corrélés (0.25), Contrepartie peu corrélée (0.25).
bscr = np.sqrt(scr_market**2 + scr_life**2 + scr_default**2 + 2*0.25*scr_market*scr_life + 2*0.25*scr_market*scr_default + 2*0.25*scr_life*scr_default)
scr_total = bscr + scr_op

# --- 2. SYNTHÈSE (RÉSULTATS) ---
st.header("2. Synthèse du Capital Requis")

col_res1, col_res2 = st.columns([1, 2])

with col_res1:
    st.metric("SCR Total", f"{scr_total:,.1f} M€")
    part_default = scr_default/scr_total if scr_total > 0 else 0
    st.metric("Part du Risque de Contrepartie", f"{part_default:.1%}", delta="Risque Dominant" if part_default > 0.5 else "Risque Dilué")

with col_res2:
    fig = go.Figure(go.Bar(
        x=["Marché", "Vie", "Contrepartie", "Opérationnel"],
        y=[scr_market, scr_life, scr_default, scr_op],
        marker_color=['blue', 'green', 'red', 'gray']
    ))
    fig.update_layout(title="Décomposition du SCR par Risque", yaxis_title="M€")
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# --- 3. DÉTAIL DES CALCULS ---
st.header("3. Détail des Modules de Risque")

st.write(f"**SCR Marché (Risque sur frais futurs UC) :** {scr_market:.1f} M€")
st.write(f"**SCR Vie (Rachat UC & Dépenses) :** {scr_life:.1f} M€")
st.write(f"**SCR Contrepartie (Défaut Maison Mère) :** {scr_default:.1f} M€")
st.caption(f"Exposition Nette : {exposure:.1f} M€ | Charge estimée : {charge_map[rating_parent]*100}%")
st.write(f"**SCR Opérationnel :** {scr_op:.1f} M€")

# --- ANALYSE STRATÉGIQUE ---
st.info("""
**Analyse du Risk Manager :**
Dans ce schéma, la solvabilité de la filiale luxembourgeoise est totalement dépendante de la santé financière de sa maison mère française.

*   **Levier d'optimisation :** La mise en place d'un **Collatéral** (nantissement de titres) permet de réduire l'exposition nette et donc d'effondrer le SCR Contrepartie.
*   **Point de vigilance :** Si la note de la maison mère se dégrade (ex: passage de A à BBB), le SCR Contrepartie explose.
""")