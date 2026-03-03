import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Gestion des Risques Opérationnels", layout="wide")

st.title("🛠️ Gestion des Risques Opérationnels")
st.subheader("Identification, Évaluation et Atténuation")

st.markdown("""
Le **Risque Opérationnel** est défini comme le risque de pertes provenant de processus internes inadéquats ou défaillants, de personnes et systèmes ou d'événements externes.
Il inclut les risques juridiques mais exclut les risques stratégiques et de réputation.
""")

st.divider()

# --- 1. CATALOGUE DES RISQUES (TAXONOMIE STANDARD) ---
st.header("1. Catalogue des Risques (Taxonomie Standard)")
st.markdown("Classification standard des événements de risques opérationnels en 7 catégories (inspirée des standards de place).")

tabs = st.tabs(["Fraude Interne", "Fraude Externe", "RH & Sécurité", "Clients & Produits", "Dommages Actifs", "Interruption Activité", "Exécution & Process"])

with tabs[0]:
    st.error("### 🕵️ Fraude Interne")
    st.write("**Définition :** Pertes dues à des actes visant à frauder, détourner des biens ou contourner la loi, impliquant au moins une partie interne.")
    st.markdown("- Détournement d'actifs\n- Falsification de documents\n- Délit d'initié\n- Vol par un employé")

with tabs[1]:
    st.error("### 🎭 Fraude Externe")
    st.write("**Définition :** Pertes dues à des actes visant à frauder, détourner des biens ou contourner la loi, par un tiers.")
    st.markdown("- Cyberattaque (Ransomware)\n- Vol de données clients\n- Falsification de chèques\n- Usurpation d'identité")

with tabs[2]:
    st.warning("### 👷 Emploi & Sécurité du Travail")
    st.write("**Définition :** Actes incompatibles avec la législation sur l'emploi ou la santé/sécurité.")
    st.markdown("- Discrimination / Harcèlement\n- Non-respect des règles de sécurité\n- Conflits sociaux\n- Erreurs de paie")

with tabs[3]:
    st.warning("### 🤝 Clients, Produits & Pratiques Commerciales")
    st.write("**Définition :** Manquement involontaire ou par négligence à une obligation professionnelle envers des clients.")
    st.markdown("- Défaut de conseil\n- Produits mal conçus (Mis-selling)\n- Blanchiment d'argent (AML)\n- Violation du secret professionnel / RGPD")

with tabs[4]:
    st.info("### 🏢 Dommages aux Actifs Physiques")
    st.write("**Définition :** Pertes dues à des dommages ou à la destruction d'actifs physiques.")
    st.markdown("- Incendie / Inondation (locaux)\n- Terrorisme\n- Vandalisme")

with tabs[5]:
    st.info("### 🛑 Interruption d'Activité & Systèmes")
    st.write("**Définition :** Pertes dues à une interruption de l'activité ou à une panne des systèmes.")
    st.markdown("- Panne matérielle / logicielle\n- Coupure télécom / énergie\n- Indisponibilité du Cloud")

with tabs[6]:
    st.success("### ⚙️ Exécution, Livraison & Gestion des Processus")
    st.write("**Définition :** Échecs dans le traitement des transactions ou la gestion des processus.")
    st.markdown("- Erreur de saisie (Fat finger)\n- Échec de reporting réglementaire\n- Litiges fournisseurs\n- Données incomplètes")

st.divider()

# --- 2. OUTIL D'AUTO-ÉVALUATION (RCSA) ---
st.header("2. Outil d'Auto-Évaluation (RCSA)")
st.markdown("**Risk and Control Self-Assessment :** Évaluez un risque spécifique pour déterminer sa criticité.")

col_input, col_viz = st.columns([1, 2])

with col_input:
    st.subheader("Évaluation du Risque Brut")
    risk_name = st.text_input("Nom du Risque", "Ex: Panne du système de gestion des sinistres")
    freq = st.select_slider("Fréquence (Probabilité)", options=["Très Faible (1)", "Faible (2)", "Moyenne (3)", "Élevée (4)", "Très Élevée (5)"], value="Faible (2)")
    impact = st.select_slider("Impact Financier (Sévérité)", options=["Négligeable (1)", "Mineur (2)", "Modéré (3)", "Majeur (4)", "Critique (5)"], value="Majeur (4)")
    
    freq_score = int(freq[-2])
    impact_score = int(impact[-2])
    
    st.subheader("Dispositif de Contrôle")
    control_quality = st.radio("Efficacité des Contrôles", ["Inexistant", "Faible", "Satisfaisant", "Fort"], index=2)
    
    control_factor = {"Inexistant": 1.0, "Faible": 0.8, "Satisfaisant": 0.5, "Fort": 0.2}
    net_score = (freq_score * impact_score) * control_factor[control_quality]

with col_viz:
    # Heatmap simple
    x = [1, 2, 3, 4, 5]
    y = [1, 2, 3, 4, 5]
    z = [[i*j for i in x] for j in y]
    
    fig = px.imshow(z, x=['1', '2', '3', '4', '5'], y=['1', '2', '3', '4', '5'], 
                    labels=dict(x="Fréquence", y="Impact", color="Score Brut"),
                    color_continuous_scale="RdYlGn_r")
    
    # Add point
    fig.add_trace(go.Scatter(x=[freq_score-1], y=[impact_score-1], mode='markers', 
                             marker=dict(color='black', size=20, symbol='x'), name='Risque Brut'))
    
    fig.update_layout(title="Matrice des Risques (Brut)", xaxis_title="Fréquence", yaxis_title="Impact")
    st.plotly_chart(fig, use_container_width=True)

# Résultat Net
st.subheader("Résultat de l'Évaluation")
col_res1, col_res2, col_res3 = st.columns(3)

col_res1.metric("Score Brut", f"{freq_score * impact_score}/25")
col_res2.metric("Réduction par Contrôles", f"-{(1-control_factor[control_quality])*100:.0f}%")
col_res3.metric("Score Net (Résiduel)", f"{net_score:.1f}/25", delta="Zone de confort" if net_score < 5 else "Action requise", delta_color="inverse")

if net_score >= 10:
    st.error("🚨 **Risque Critique :** Plan d'action immédiat requis (Renforcement des contrôles, Assurance, ou Abandon de l'activité).")
elif net_score >= 5:
    st.warning("⚠️ **Risque Significatif :** Surveillance accrue et amélioration des contrôles recommandée.")
else:
    st.success("✅ **Risque Maîtrisé :** Niveau acceptable.")

st.divider()

# --- 3. GESTION DES INCIDENTS ---
st.header("3. Gestion des Incidents (Base de Pertes)")
st.markdown("Le suivi des pertes avérées est essentiel pour calibrer les modèles de capital (LDA - Loss Distribution Approach).")

# Exemple de base de données
data_incidents = pd.DataFrame({
    "Date": ["2023-01-15", "2023-03-22", "2023-06-10", "2023-09-05", "2023-11-20"],
    "Type": ["Exécution", "Fraude Externe", "Interruption", "Clients", "RH"],
    "Montant Perte (€)": [15000, 450000, 120000, 5000, 25000],
    "Statut": ["Clôturé", "En cours", "Clôturé", "Clôturé", "En cours"]
})

st.dataframe(data_incidents)

st.info("💡 **Lien avec le SCR Opérationnel :** Bien que la Formule Standard soit forfaitaire (basée sur les primes/provisions), la collecte des pertes historiques est obligatoire pour valider la pertinence de cette formule standard par rapport au profil de risque réel.")

with st.expander("📚 Comprendre la méthode LDA (Loss Distribution Approach)", expanded=True):
    st.markdown("""
    La méthode **LDA** est l'approche standard pour modéliser le capital économique pour le risque opérationnel (Modèle Interne).
    Elle repose sur la convolution de deux distributions :
    
    1.  **Distribution de Fréquence :** Combien d'incidents surviennent par an ? (ex: Loi de Poisson $\lambda$).
    2.  **Distribution de Sévérité :** Quel est le coût d'un incident quand il survient ? (ex: Loi Lognormale ou Pareto pour les queues épaisses).
    
    **Le processus :**
    On simule des milliers d'années d'activité (Monte Carlo). Pour chaque année, on tire un nombre de sinistres, puis un coût pour chaque sinistre. La somme donne la perte annuelle totale.
    
    En Modèle Interne, le **SCR Opérationnel** correspond à la VaR 99.5% de cette distribution agrégée des pertes annuelles.
    """)
