import streamlit as st
import pandas as pd

st.set_page_config(page_title="Normes Comptables", layout="wide")

st.title("Panorama des Normes Comptables")
st.subheader("Cohabitation des référentiels : French GAAP, Solvabilité II, IFRS 17 et IFRS 9")

st.markdown("""
En analyse actuarielle, la valorisation d'un contrat d'assurance dépend directement du cadre d'évaluation retenu.
Un même portefeuille présentera ainsi trois lectures distinctes selon la finalité poursuivie :
1. **Garantir la prudence et la pérennité statutaire** (Normes françaises / Code des Assurances).
2. **Assurer la solvabilité et la protection des assurés** en valeur de marché (Solvabilité II).
3. **Mesurer la performance économique et la rentabilité contractuelle** (IFRS 17).
""")

st.divider()

# Onglets pour structurer l'explication
tab1, tab2, tab3, tab4 = st.tabs(["French GAAP (Social)", "Solvabilité II (Prudentiel)", "IFRS 17 (Passif)", "IFRS 9 (Actif)"])

with tab1:
    st.header("1. Normes Françaises (Code des Assurances)")
    st.markdown("""
    ### Le Socle Historique (Comptabilité Sociale)
    Référentiel utilisé pour les comptes statutaires et la fiscalité en France. Il est régi par le **Code des Assurances** et le plan comptable des assurances.
    
    #### Principe Directeur : La Prudence
    L'objectif prioritaire est de protéger les assurés en évitant la distribution de bénéfices non réalisés.
    * **Approche statique :** Les engagements sont évalués sur la base de tables de mortalité et de taux d'intérêt fixés à la souscription (taux technique).
    * **Asymétrie :** Les moins-values latentes sur les actifs font l'objet de dotations aux provisions (PDD, PRE), tandis que les plus-values latentes ne sont pas comptabilisées au bilan (hors annexe).
    
    #### Les Briques du Passif
    1. **Provisions Mathématiques (PM) :** Valeur actuelle des engagements de l'assureur vis-à-vis des assurés.
       * *Définition (Art. R331-3) :* Différence entre les valeurs actuelles des engagements respectifs de l'assureur et des assurés.
       * *Méthodes :* **Prospective** (V.A. Prestations - V.A. Primes) ou **Rétrospective** (capitalisation des primes passées, usuel en épargne).
       * *Taux :* Taux technique garanti fixé à la souscription.
    2. **Provision pour Participation aux Bénéfices (PPB) :** Spécificité majeure du cadre français.
       * L'assureur a l'obligation réglementaire de redistribuer une quote-part minimale des bénéfices financiers et techniques aux assurés.
       * La PPB permet de différer cette attribution dans un délai maximal de **8 ans**, constituant un amortisseur essentiel pour lisser les rendements servis.
    3. **Réserve de Capitalisation (RC) :** Spécifique au portefeuille obligataire.
       * Les plus-values réalisées sur cessions d'obligations sont affectées à cette réserve sans transiter par le résultat distribuable.
       * Les moins-values constatées sont compensées par une reprise équivalente sur la réserve.
    4. **Provisions de Sécurité :**
       * **PDD (Dépréciation Durable) :** Concerne les actifs non amortissables (actions, immobilier) en cas de dépréciation prolongée.
       * **PRE (Risque d'Exigibilité) :** Dotée lorsque la valeur de marché globale des actifs devient inférieure à la valeur comptable nette.
       * **PAF (Aléas Financiers) :** Dotée si le rendement anticipé des actifs est jugé insuffisant pour honorer les taux garantis.
    """)
    st.info("**Enjeu de marché :** Dans un contexte de volatilité des taux longs, le stock de plus-values latentes obligataires fluctue fortement, ce qui renforce l'importance prudentielle de la réserve de capitalisation et de la PRE.")

with tab2:
    st.header("2. Solvabilité II (Réglementation Européenne)")
    st.markdown("""
    ### La Vision Économique et Prudentielle
    Directive européenne (2009/138/CE) en vigueur depuis 2016. Elle instaure une gouvernance et une évaluation fondées sur la réalité économique des risques.
    
    #### Les Trois Piliers
    * **Pilier 1 (Quantitatif) :** Exigences de capital réglementaire (SCR / MCR) et valorisation en juste valeur du bilan (Balance Sheet).
    * **Pilier 2 (Gouvernance) :** Système de gestion des risques, auto-évaluation prospective des risques et de la solvabilité (ORSA), fonctions clés (actuarielle, gestion des risques, audit, conformité).
    * **Pilier 3 (Transparence & Reporting) :** Rapports destinés au superviseur (RSR, QRT) et au marché (SFCR).

    #### Le Bilan en Juste Valeur (Market Consistent)
    * **Actif :** Évaluation à la valeur de marché (Mark-to-Market ou Mark-to-Model).
    * **Passif (Best Estimate - BEL) :** Projection prospective des flux de trésorerie probabilisés (primes, prestations, rachats, frais) actualisés sur la courbe des taux sans risque fournie par l'EIOPA.
    * **Marge de Risque (Risk Margin) :** Coût du capital théorique requis pour transférer les engagements à un tiers repreneur (coût du capital fixé à 6% des SCR futurs non hedgeables).

    #### Le Ratio de Solvabilité
    $$ \\text{Ratio Solvabilité II} = \\frac{\\text{Fonds Propres Éligibles (Eligible Own Funds)}}{\\text{SCR (Solvency Capital Requirement)}} $$
    * **SCR :** Capital requis pour absorber une perte bicentenaire à horizon 1 an (VaR 99.5%).
    * **MCR (Minimum Capital Requirement) :** Seuil prudentiel minimal déclenchant le retrait d'agrément en cas de non-respect.
    """)
    st.info("**Mesures contracycliques :** Afin d'atténuer la volatilité artificielle du bilan économique lors des chocs de spread, la directive prévoit des mécanismes d'ajustement, notamment le Volatility Adjustment (VA) et le Matching Adjustment (MA).")

with tab3:
    st.header("3. IFRS 17 (Norme Comptable Internationale)")
    st.markdown("""
    ### La Vision Financière et la Reconnaissance du Profit
    Norme comptable internationale (IASB) applicable depuis le 1er janvier 2023 pour la comptabilisation des contrats d'assurance, venant remplacer IFRS 4.
    
    #### Objectifs : Comparabilité et Transparence
    Harmoniser la présentation des états financiers au niveau mondial et aligner la comptabilisation des contrats d'assurance sur les principes d'engagement et de marge de service.
    
    #### Le Modèle Général d'Évaluation (General Measurement Model - GMM)
    Le passif relatif à la couverture résiduelle (LRC - Liability for Remaining Coverage) s'articule autour de trois composantes :
    1. **Flux de trésorerie d'exécution (Fulfilment Cash Flows - FCF) :**
       * *Estimations courantes :* Moyenne pondérée par les probabilités des flux futurs actualisés.
       * *Ajustement pour Risque non-financier (Risk Adjustment - RA) :* Rémunération exigée face à l'incertitude des flux biométriques et opérationnels.
       * *Actualisation :* Courbe sans risque ajustée d'une prime d'illiquidité (approche Bottom-up ou Top-down).
    2. **Marge de Service Contractuelle (Contractual Service Margin - CSM) :**
       * Représente le profit attendu non encore acquis à l'origine du contrat.
       * Aucun bénéfice immédiat n'est comptabilisé à l'émission : il est mis en réserve dans la CSM et reconnu progressivement au fur et à mesure du service rendu (Coverage Units).
       * En cas de souscription déficitaire (groupe de contrats onéreux), la perte est immédiatement constatée en résultat.

    #### Modèles Dérivés
    * **GMM (General Model) :** Modèle standard pour les contrats d'assurance vie longue et prévoyance.
    * **VFA (Variable Fee Approach) :** Dédié aux contrats à participation directe (fonds en euros, unités de compte), où l'assureur perçoit une rémunération proportionnelle aux actifs sous-jacents.
    * **PAA (Premium Allocation Approach) :** Modèle simplifié réservé aux contrats de courte durée (< 1 an), usuel en assurance non-vie.
    """)
    st.info("**Changement de paradigme :** Les primes émises ne constituent plus le chiffre d'affaires en IFRS 17. Le compte de résultat présente désormais un « revenu d'assurance » reflétant la couverture effectivement délivrée sur la période.")

with tab4:
    st.header("4. IFRS 9 (Instruments Financiers)")
    st.markdown("""
    ### La Vision Actif et le Risque de Crédit
    Norme internationale régissant la classification, la valorisation et la dépréciation des actifs financiers, entrée en application conjointe avec IFRS 17 chez les assureurs.
    
    #### Classification & Évaluation
    La comptabilisation repose sur le modèle de gestion (Business Model) et la nature des flux contractuels (critère SPPI) :
    1. **Coût Amorti :** Titres détenus pour percevoir les flux contractuels sans intention de revente anticipée.
    2. **Juste Valeur par Capitaux Propres (FVOCI) :** Actifs dont l'objectif est à la fois la collecte des coupons et la cession (gestion ALM active). Les variations de valeur n'affectent pas le compte de résultat net.
    3. **Juste Valeur par Résultat (FVTPL) :** Dérivés, actions et OPCVM ne satisfaisant pas le critère SPPI.
    
    #### Modèle de Pertes Attendues (Expected Credit Loss - ECL)
    Remplacement du modèle de pertes avérées par une approche prospective :
    * **Étape 1 (Stage 1) :** Provisionnement des pertes attendues à horizon 12 mois pour les actifs sans dégradation significative.
    * **Étape 2 (Stage 2) :** Provisionnement des pertes attendues à maturité en cas d'augmentation significative du risque de crédit depuis l'origine.
    * **Étape 3 (Stage 3) :** Actifs en défaut avéré.
    """)
    st.info("**Mise en miroir Actif / Passif :** L'activation de l'option OCI en IFRS 9 permet de neutraliser l'impact de la volatilité des taux sur les capitaux propres, en symétrie avec l'option OCI offerte par IFRS 17 au passif.")

st.divider()

# Tableau Comparatif
st.header("Synthèse Comparative des Référentiels")

data = {
    "Dimension": ["Objectif Principal", "Valorisation Actif", "Valorisation Passif", "Actualisation", "Indicateur Clé"],
    "French GAAP": ["Prudence et distribution", "Coût historique amorti", "Taux technique garanti", "Taux contractuel fixe", "Résultat net comptable"],
    "Solvabilité II": ["Protection des assurés", "Valeur de marché (Fair Value)", "Best Estimate + Marge de risque", "Courbe des taux sans risque (EIOPA)", "Ratio de solvabilité (SCR)"],
    "IFRS 17": ["Transparence de performance", "Valeur de marché", "FCF (Flux + RA) + CSM", "Courbe ajustée de l'illiquidité", "Marge de service (CSM)"],
    "IFRS 9": ["Juste valeur des instruments", "Coût amorti / FVOCI / FVTPL", "Sans objet (norme actif)", "Taux effectif / Taux de marché", "Coût du risque (ECL)"]
}

df = pd.DataFrame(data)
st.table(df)

