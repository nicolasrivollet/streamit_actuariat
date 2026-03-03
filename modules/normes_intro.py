import streamlit as st
import pandas as pd

st.set_page_config(page_title="Normes Comptables", layout="wide")

st.title("📚 Panorama des Normes Comptables")
st.subheader("Comprendre la cohabitation des référentiels : French GAAP, Solvabilité II, IFRS 17")

st.markdown("""
En tant qu'actuaire, il est fondamental de comprendre que **la valeur d'un contrat d'assurance dépend des lunettes avec lesquelles on le regarde**.
Un même portefeuille peut avoir trois valeurs différentes selon l'objectif recherché :
1.  **Garantir la prudence** (Normes Françaises / Code des Assurances).
2.  **Assurer la solvabilité** en cas de faillite immédiate (Solvabilité II).
3.  **Mesurer la rentabilité économique** réelle (IFRS 17).
""")

st.divider()

# Onglets pour structurer l'explication
tab1, tab2, tab3, tab4 = st.tabs(["🇫🇷 French GAAP (Social)", "🇪🇺 Solvabilité II (Prudentiel)", "🌍 IFRS 17 (Passif)", "📉 IFRS 9 (Actif)"])

with tab1:
    st.header("1. Normes Françaises (Code des Assurances)")
    st.markdown("""
    ### 🏛️ Le Socle Historique (Comptabilité Sociale)
    C'est le référentiel utilisé pour les comptes statutaires et la fiscalité en France. Il est régi par le **Code des Assurances** et le plan comptable des assurances.
    
    #### 🛡️ Principe Directeur : La Prudence
    L'objectif est de protéger les assurés en évitant de distribuer des bénéfices fictifs.
    *   **Approche statique :** Les engagements sont souvent évalués sur la base de tables de mortalité et de taux d'intérêt fixés à la souscription (Taux Technique).
    *   **Asymétrie :** Les moins-values latentes sur les actifs sont provisionnées (PPD/PRE), mais les plus-values latentes ne sont pas comptabilisées au bilan (hors annexe).
    
    #### 🧱 Les Briques du Passif
    1.  **Provisions Mathématiques (PM) :** C'est la valeur actuelle des engagements de l'assureur vis-à-vis des assurés.
        *   *Définition (Art. R331-3) :* Différence entre les valeurs actuelles des engagements de l'assureur et des assurés.
        *   *Méthodes :* **Prospective** (V.A. Prestations - V.A. Primes) ou **Rétrospective** (Capitalisation des primes passées, usuel en Épargne).
        *   *Taux :* Taux technique garanti (fixé à la souscription).
    2.  **Provision pour Participation aux Bénéfices (PPB) :** Spécificité française cruciale.
        *   L'assureur a l'obligation légale de redistribuer une part des bénéfices financiers et techniques aux assurés.
        *   Il peut stocker ces bénéfices en PPB et a **8 ans** pour les redistribuer. C'est un outil majeur de lissage des taux servis.
    3.  **Réserve de Capitalisation (RC) :** Spécifique aux obligations.
        *   Les **plus-values réalisées** sur les ventes d'obligations ne vont pas en résultat mais alimentent cette réserve.
        *   Les **moins-values réalisées** sont compensées par une reprise sur cette réserve.
        *   *But :* Lisser le rendement obligataire et éviter les arbitrages opportunistes liés aux taux.
    4.  **Provisions de Sécurité :**
        *   **PDD (Dépréciation Durable) :** Concerne les actifs non amortissables (Actions, Immo). Si la valeur de marché reste durablement inférieure au prix d'achat, la moins-value latente est provisionnée.
        *   **PRE (Risque d'Exigibilité) :** Dotée si la valeur de marché des actifs < valeur comptable (krach obligataire/actions).
        *   **PAF (Aléas Financiers) :** Dotée si l'assureur anticipe que le rendement futur de ses actifs sera insuffisant pour servir les taux garantis aux assurés.
    """)
    st.info("💡 **Enjeu Actuel :** Avec la remontée des taux, le stock de plus-values latentes obligataires fond, rendant la dotation de la PRE potentiellement nécessaire pour certains acteurs.")

with tab2:
    st.header("2. Solvabilité II (Réglementation Européenne)")
    st.markdown("""
    ### 🇪🇺 La Vision Économique (Risque)
    Directive européenne (2009/138/CE) appliquée depuis 2016. Elle impose une gestion basée sur les risques réels et non plus sur des règles forfaitaires.
    
    #### 🏗️ Les 3 Piliers
    *   **Pilier 1 (Quantitatif) :** Calcul des exigences de capital (SCR/MCR) et valorisation du bilan.
    *   **Pilier 2 (Gouvernance) :** Système de gestion des risques, ORSA (Auto-évaluation), Fonction Actuarielle.
    *   **Pilier 3 (Reporting) :** Transparence vers le superviseur (RSR, QRT) et le public (SFCR).

    #### ⚖️ Le Bilan "Market Consistent"
    Tout est valorisé à la valeur de marché (Fair Value).
    *   **Actif :** Valeur de marché (Mark-to-Market ou Mark-to-Model).
    *   **Passif (Best Estimate - BEL) :** Projection réaliste des flux de trésorerie (primes, sinistres, rachats, frais) actualisée par la courbe des taux sans risque (EIOPA).
    *   **Marge de Risque (Risk Margin) :** Coût du capital nécessaire pour céder les engagements à un tiers (6% des SCR futurs actualisés).

    #### 📉 Le Ratio de Solvabilité
    $$ \\text{Ratio S2} = \\frac{\\text{Fonds Propres Éligibles (Own Funds)}}{\\text{SCR (Solvency Capital Requirement)}} $$
    *   **SCR :** Capital nécessaire pour absorber un choc bicentenaire (VaR 99.5% à 1 an).
    *   **MCR :** Seuil critique de capital en dessous duquel l'agrément est retiré.
    """)
    st.success("💡 **Impact :** La volatilité des marchés impacte directement le ratio S2. C'est pourquoi des mesures contracycliques (Volatility Adjustment, mesures transitoires) existent.")

with tab3:
    st.header("3. IFRS 17 (Normes Internationales)")
    st.markdown("""
    ### 🌍 La Vision Financière (Performance)
    Norme comptable internationale (IASB) pour les contrats d'assurance, obligatoire depuis le 01/01/2023. Elle remplace IFRS 4.
    
    #### 🎯 Objectif : Lisibilité et Comparabilité
    Fini le "Black Box" de l'assurance. IFRS 17 aligne la comptabilité assurance sur les standards industriels (reconnaissance du revenu au fil de l'eau).
    
    #### 🧩 Le Modèle Général (General Measurement Model - GMM)
    Le passif (LRC - Liability for Remaining Coverage) est la somme de 3 blocs :
    1.  **Flux de trésorerie d'exécution (FCF) :**
        *   *Estimations courantes* : Moyenne pondérée des flux futurs (proche du Best Estimate S2).
        *   *Ajustement pour Risque (RA)* : Compensation pour l'incertitude non-financière (≠ Marge de Risque S2).
        *   *Actualisation* : Taux sans risque + Prime d'illiquidité (Bottom-up) ou Taux portefeuille - Risque crédit (Top-down).
    2.  **Marge de Service Contractuelle (CSM) :**
        *   Représente le **profit non gagné** du contrat.
        *   Au jour 1, aucun profit n'est enregistré : il est stocké dans la CSM.
        *   *Amortissement* : La CSM est libérée en résultat via des **Unités de Couverture** (Coverage Units).
        *   *Exception* : Si le contrat est déficitaire (Onéreux), la perte est immédiate (pas de CSM).

    #### 🚦 Modèles de Mesure
    *   **GMM (General Model) :** Le modèle par défaut (Vie, Prévoyance longue).
    *   **VFA (Variable Fee Approach) :** Pour les contrats avec participation directe (Unités de Compte, Fonds Euros), où l'assureur partage le rendement avec l'assuré.
    *   **PAA (Premium Allocation) :** Modèle simplifié pour les contrats courts (< 1 an), proche de l'approche primes acquises (Non-Vie).
    """)
    st.warning("💡 **Révolution :** Le Chiffre d'Affaires (Primes Émises) disparaît du compte de résultat au profit du 'Revenu d'Assurance'.")

with tab4:
    st.header("4. IFRS 9 (Instruments Financiers)")
    st.markdown("""
    ### 📉 La Vision Actif (Risque de Crédit)
    Norme internationale pour la comptabilisation des instruments financiers, entrée en vigueur en 2018 (mais appliquée en 2023 pour les assureurs, en même temps qu'IFRS 17).
    
    #### 🏷️ Classification & Mesure
    La manière dont un actif est valorisé dépend de son **Business Model** et de ses caractéristiques contractuelles (Test SPPI) :
    1.  **Coût Amorti :** Pour les prêts simples détenus jusqu'à l'échéance.
    2.  **FVOCI (Fair Value through OCI) :** Juste valeur au bilan, mais les variations vont en Capitaux Propres (OCI - Other Comprehensive Income). Idéal pour les obligations des assureurs (évite la volatilité du P&L).
    3.  **FVTPL (Fair Value through P&L) :** Juste valeur au bilan, variations en Résultat. Obligatoire pour les actions et dérivés.
    
    #### 🔮 Dépréciation (Impairment)
    Passage d'un modèle de "pertes avérées" à un modèle de **"pertes attendues" (ECL - Expected Credit Loss)**.
    *   **Stage 1 (Sain) :** Provisionnement des pertes attendues à 12 mois.
    *   **Stage 2 (Dégradation significative) :** Provisionnement des pertes attendues à maturité (Lifetime ECL).
    *   **Stage 3 (Défaut) :** Actif déprécié.
    """)
    st.info("💡 **Interaction Actif/Passif :** L'option 'OCI' d'IFRS 9 permet de limiter la volatilité du résultat net, en miroir de l'option OCI d'IFRS 17 pour le passif.")

st.divider()

# Tableau Comparatif
st.header("⚔️ Synthèse Comparative")

data = {
    "Critère": ["Objectif Principal", "Valorisation Actif", "Valorisation Passif", "Actualisation", "Indicateur Clé"],
    "French GAAP": ["Prudence & Impôt", "Coût Historique (amorti)", "Taux Technique Garanti", "Taux historique (fixe)", "Résultat Net Comptable"],
    "Solvabilité II": ["Protection Assuré (Faillite)", "Valeur de Marché", "Best Estimate (Flux probables)", "Courbe Taux Sans Risque", "Ratio de Solvabilité (SCR)"],
    "IFRS 17": ["Information Financière", "Valeur de Marché", "FCF (Flux + RA) + CSM", "Taux ajusté (Illiquidité)", "Marge de Service (CSM)"],
    "IFRS 9": ["Information Financière", "Juste Valeur (Majorité)", "N/A (Concerne l'Actif)", "N/A", "Coût du Risque (ECL)"]
}

df = pd.DataFrame(data)
st.table(df)
