import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import smithwilson as sw

# --- CONFIGURATION DE LA PAGE ---
# Note : st.set_page_config est géré par Accueil.py, ne pas le remettre ici si intégré au multipage.



# --- INTERFACE UTILISATEUR ---

st.title("Calculateur Réel Smith-Wilson")
st.markdown("""
Cette page implémente l'algorithme d'extrapolation de la courbe des taux tel que prescrit par la réglementation **Solvabilité II**. 
Contrairement aux modèles de lissage, Smith-Wilson garantit une **interpolation exacte** des points de marché liquides.
""")

st.divider()

# --- INPUTS ---
col_in1, col_in2 = st.columns([1, 2])

with col_in1:
    st.subheader("Données de Marché")
    st.write("Modifiez les taux pour recalculer la courbe :")
    df_market = pd.DataFrame({
        'Maturité': [1.0, 2.0, 5.0, 10.0, 20.0],
        'Taux (%)': [2.50, 2.75, 3.10, 3.45, 3.85]
    })
    edited_df = st.data_editor(df_market, num_rows="dynamic")
    
    st.subheader("Paramètres EIOPA")
    ufr_val = st.slider("Ultimate Forward Rate (UFR) %", 2.0, 5.0, 3.45, step=0.05) / 100
    alpha_val = st.slider("Vitesse de Convergence (Alpha)", 0.05, 0.50, 0.15, step=0.01)
    llp = edited_df['Maturité'].max()

with col_in2:
    st.subheader("Visualisation de l'Extrapolation")
    
    t_market = edited_df['Maturité'].values
    r_market = edited_df['Taux (%)'].values / 100
    t_target = np.linspace(0.5, 60, 200) # Projection jusqu'à 60 ans
    
    try:
        # y_target = compute_smith_wilson(t_target, t_market, r_market, alpha_val, ufr_val)
        
        y_target = np.array(sw.fit_smithwilson_rates(rates_obs=r_market, t_obs=t_market,
                                                t_target=t_target, ufr=ufr_val,
                                                alpha=alpha_val)).flatten()  # Optional

        fig = go.Figure()

        # Zone Liquide vs Extrapolation
        fig.add_vrect(x0=0, x1=llp, fillcolor="green", opacity=0.05, line_width=0, annotation_text="Zone Liquide")
        fig.add_vrect(x0=llp, x1=60, fillcolor="blue", opacity=0.05, line_width=0, annotation_text="Extrapolation")
        
        # Courbe Smith-Wilson
        fig.add_trace(go.Scatter(x=t_target, y=y_target*100, name="Courbe S-W", line=dict(color='#1E88E5', width=4)))
        
        # Points de Marché
        fig.add_trace(go.Scatter(x=t_market, y=r_market*100, name="Marché (Inputs)", mode='markers', marker=dict(color='red', size=10, symbol='diamond')))
        
        # Ligne UFR
        fig.add_hline(y=ufr_val*100, line_dash="dash", line_color="orange", annotation_text="Cible UFR")

        fig.update_layout(
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis_title="Maturité (Années)",
            yaxis_title="Taux Actuariel (%)",
            legend=dict(yanchor="bottom", y=0.01, xanchor="right", x=0.99),
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Erreur de calcul : {e}. Assurez-vous que les maturités sont positives et croissantes.")

st.markdown(f"""
    * **UFR ({ufr_val}%)** : Le taux vers lequel la courbe doit converger à l'infini. Il reflète les anticipations de croissance et d'inflation de long terme.
    * **LLP ({df_market['Maturité'].max()} ans)** : La maturité maximale où le marché est considéré comme profond et liquide.
    * **Alpha ({alpha_val})** : Détermine la vitesse à laquelle la courbe rejoint l'UFR après le LLP. Un alpha élevé signifie une convergence rapide.
    """)

st.divider()

# --- ANALYSE DE ROBUSTESSE ---
st.header("Analyse de la Calibration")

check_col1, check_col2, check_col3 = st.columns(3)


with check_col1:
    # Test d'interpolation sur le point 10 ans
    val_10y = sw.fit_smithwilson_rates(rates_obs=r_market, t_obs=t_market, t_target=t_target, ufr=ufr_val, alpha=alpha_val)[33] 
    st.metric("Taux à 10 ans (Calculé)", f"{y_target[32]*100:.2f}%")
    st.caption("Doit être strictement égal au taux d'entrée.")

with check_col2:
    st.metric("Convergence à 60 ans", f"{y_target[-1]*100:.2f}%")
    st.caption(f"Cible UFR : {ufr_val*100:.2f}%")

with check_col3:
    st.metric("Dernier Point Liquide (LLP)", f"{llp} ans")
    st.caption("Début de l'extrapolation.")

# --- FOOTER TECHNIQUE ---
with st.expander("📚 Détails méthodologiques et mathématiques", expanded=True):
    st.write("""
    Le modèle Smith-Wilson est une méthode d'ajustement de la structure par terme des taux qui minimise une fonction de rugosité sous contraintes d'interpolation.
    
    **Pourquoi est-ce une 'Boîte Noire' ?**
    Le calcul repose sur l'inversion de la matrice de noyau $W$. Contrairement à Nelson-Siegel, il n'y a pas de paramètres globaux (niveau, pente). Chaque point de marché influence localement la courbe via un poids $\zeta_i$. 
    
    **Le rôle de l'Alpha :**
    C'est le paramètre de tension. S'il est trop faible, la courbe mettra trop de temps à rejoindre l'UFR. S'il est trop élevé, la courbe peut présenter des oscillations brutales des taux 'Forward' juste après le LLP.
    """)

st.header("Mécanisme de calcul")

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


st.info("**Conformité S2** : Pour les assureurs européens, cette courbe est fournie mensuellement par l'EIOPA. L'enjeu pour l'actuaire n'est pas de la recréer, mais de comprendre sa sensibilité aux changements de paramètres réglementaires.")