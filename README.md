# 📊 Portfolio Actuariat & Gestion des Risques

**Auteur :** Nicolas Rivollet  
**Stack :** Python, Streamlit, Plotly, NumPy, Pandas, SciPy, scikit-learn

## 🎯 Objectif du Projet

Cette application web interactive montre comment la **Data Science** et le **développement logiciel** s'appliquent aux problématiques actuarielles et de gestion des risques.

Elle sert de vitrine pour des compétences en :
*   **Modélisation Financière :** Courbes de taux, GSE, valorisation d'options, mesures de risque de marché.
*   **Solvabilité II :** Piliers 1, 2 et 3 (SCR, ORSA, Qualité des données).
*   **Gestion des Risques :** Appétence au risque, risques opérationnels, allocation d'actifs.
*   **Réglementation & ESG :** DORA, CSRD, Risque Climatique.

Chaque module combine un rappel théorique (formules, cadre réglementaire), des paramètres ajustables et des visualisations Plotly. Les données utilisées sont simulées ou intégrées au code.

## 🗂 Structure de l'Application

L'application compte 4 sections, accessibles depuis le menu latéral :

### 1. 🏠 Accueil & Cadre Général
*   **Présentation :** Page d'accueil du portfolio.
*   **Panorama des Normes Comptables :** Comparatif French GAAP / Solvabilité II / IFRS 17.
*   **Les 3 Piliers Solvabilité II :** Vision globale de la directive.
*   **Architecture Réglementaire :** Hiérarchie des normes (processus Lamfalussy).
*   **Assurance Vie Luxembourg :** Triangle de sécurité, FID/FAS, gestion de fortune.

### 2. 📈 Modélisation Financière
*   **Modélisation Courbe de Taux (intro) :** Comparatif des méthodologies de construction de courbe.
*   **Modèle Nelson-Siegel :** Calibration d'une courbe de taux.
*   **Modèle Smith-Wilson :** Extrapolation de la courbe (UFR).
*   **Générateur de Scénarios Économiques (GSE) :** Simulation stochastique.
*   **Modèle Black-Scholes :** Valorisation d'options européennes et calcul des grecques.
*   **Modèles Risque de Marché :** VaR, SVaR, IRC, CRM.
*   **Théorie GLM :** Modèles linéaires généralisés appliqués à la tarification.
*   **Lois de Probabilités :** Principales distributions utilisées en actuariat.

### 3. 🛡️ Risques & Allocation de Capital
*   **Tableau de Bord Risques Financiers :** Suivi de l'allocation et des risques de marché.
*   **Classes d'Actifs & Risques :** Cartographie Rendement / Risque.
*   **SCR Global (Agrégation) :** Agrégation des modules de risque via matrice de corrélation.
*   **SCR Taux (Standard) :** Choc de taux (Up/Down) sur la NAV.
*   **SCR Asset Screener :** Impact en capital d'un nouvel investissement.
*   **Sélection Supports UC :** Critères de référencement des unités de compte.
*   **SCR Lux (Réassurance) :** Filiale luxembourgeoise réassurée à 100 % en intra-groupe.

### 4. ⚖️ Gouvernance & Prospective
*   **Réforme Solvabilité II :** Impacts de la revue 2020.
*   **Processus ORSA :** Simulation de trajectoires de solvabilité.
*   **Appétence au Risque (RAF) :** Cockpit des indicateurs clés (KRI).
*   **Risques Opérationnels :** Cartographie et auto-évaluation (RCSA).
*   **Réglementation DORA :** Résilience opérationnelle numérique.
*   **Reporting CSRD :** Reporting extra-financier et double matérialité.
*   **Qualité des Données S2 :** Gouvernance et critères d'exhaustivité, d'exactitude et de pertinence.
*   **ESG & Investissements :** Stratégies durables et simulation d'impact.
*   **Risque Climatique (Cat Nat) :** Cartographie des impacts.

### 🚧 Modules non référencés dans le menu

Les modules suivants sont présents dans le dossier `modules/` mais ne figurent pas dans la navigation :

| Fichier | Sujet |
|---|---|
| `best_estimate_vie.py` | Best Estimate Vie : projection des flux de trésorerie |
| `ifrs17_csm.py` | Moteur IFRS 17 : simulation de la CSM (GMM) |
| `ifrs9_standard.py` | IFRS 9 : instruments financiers et provisionnement du risque de crédit |
| `mortalite_lee_carter.py` | Mortalité : projection stochastique Lee-Carter |
| `provisionnement_IARD.py` | Provisionnement Non-Vie : Chain-Ladder et IBNR |
| `pilotage_reassu.py` | Pilotage Réassurance : optimisation d'une structure XL |
| `volatility_adjustment.py` | Volatility Adjustment : impact sur le bilan |
| `alm_simulator.py` | Simulateur ALM : projection d'un fonds euros et participation aux bénéfices |
| `pricing_glm_xgb.py` | Tarification Non-Vie : GLM vs Machine Learning |
| `bale3_regulation.py` | Bâle III : réglementation prudentielle bancaire |

## 📁 Organisation du Code

```
.
├── Accueil.py          # Point d'entrée : page d'accueil et navigation (st.navigation)
├── modules/            # Une page Streamlit autonome par fichier
├── requirements.txt    # Dépendances (versions figées)
└── .devcontainer/      # Configuration GitHub Codespaces / Dev Containers
```

Pour ajouter une page : créer un fichier dans `modules/`, déclarer un `st.Page` dans `Accueil.py`, puis l'ajouter à la section voulue du dictionnaire `pages`.

## 🚀 Installation et Lancement

### Pré-requis
*   Python 3.11 ou supérieur

### Installation des dépendances
```bash
pip install -r requirements.txt
```

### Lancement de l'application
```bash
streamlit run Accueil.py
```

L'application est ensuite accessible sur http://localhost:8501.

## 🛠 Bibliothèques Principales

*   `streamlit` : Framework d'interface web et navigation multi-pages.
*   `plotly` : Visualisations interactives.
*   `numpy` / `pandas` : Calcul matriciel et manipulation de données.
*   `scipy` : Optimisation (calibration Nelson-Siegel) et lois statistiques.
*   `smithwilson` : Moteur d'extrapolation des taux.
*   `scikit-learn` / `statsmodels` : GLM et modèles de Machine Learning pour la tarification.

---
*Ce projet a été développé dans un but pédagogique et de démonstration professionnelle.*
