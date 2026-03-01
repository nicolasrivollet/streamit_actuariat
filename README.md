# 📊 Portfolio Actuariat & Data Science

**Auteur :** Nicolas Rivollet  
**Stack :** Python, Streamlit, Plotly, NumPy, Pandas

## 🎯 Objectif du Projet

Ce projet est une application web interactive démontrant l'application de techniques de **Data Science** et de **développement logiciel** aux problématiques actuarielles modernes.

Il sert de support de démonstration pour des compétences en :
*   **Modélisation Financière :** Courbes de taux, GSE, Allocation d'actifs.
*   **Solvabilité II :** Piliers 1, 2 et 3 (SCR, ORSA, Qualité des données).
*   **Assurance Vie & Non-Vie :** Provisionnement, Tarification, IFRS 17.
*   **Réglementation & ESG :** DORA, CSRD, Risque Climatique.

## 🗂 Structure de l'Application

L'application est structurée en 4 pôles métiers accessibles via la navigation :

### 1. 🏠 Présentation & Cadre
*   **Panorama des Normes :** Comparatif French GAAP / S2 / IFRS 17.
*   **Les 3 Piliers S2 :** Vision globale de la directive.
*   **Architecture Réglementaire :** Hiérarchie des normes (Lamfalussy).

### 2. ⚖️ Focus Réglementaire & ESG
*   **Réforme S2 :** Impacts de la revue 2020.
*   **Processus ORSA :** Simulation de trajectoires de solvabilité.
*   **Appétence au Risque (RAF) :** Cockpit des indicateurs clés (KRI).
*   **Risques Opérationnels :** Cartographie et auto-évaluation (RCSA).
*   **DORA :** Résilience opérationnelle numérique.
*   **CSRD :** Reporting extra-financier et double matérialité.
*   **Qualité des Données :** Gouvernance et critères ACA.
*   **ESG & Investissements :** Stratégies durables et simulation d'impact.
*   **Risque Climatique :** Cartographie des impacts Cat Nat.

### 3. 📈 Finance & Actif
*   **Tableau de Bord Risques :** Suivi de l'allocation et des risques de marché.
*   **Classes d'Actifs :** Cartographie Rendement / Risque.
*   **Générateur Scénarios Eco (GSE) :** Modélisation stochastique (Black-Scholes).
*   **SCR Asset Screener :** Analyse d'impact en capital d'un nouvel investissement.
*   **SCR Taux :** Calcul du choc de taux (Up/Down) sur la NAV.
*   **Volatility Adjustment :** Simulation de l'impact sur le bilan.
*   **Modèles de Taux :** Nelson-Siegel (Calibration) et Smith-Wilson (Extrapolation).

### 4. 🛡️ Passif & Solvabilité
*   **Best Estimate Vie :** Projection des flux de trésorerie (Cash Flows).
*   **Moteur IFRS 17 :** Simulation de la CSM (GMM).
*   **Mortalité (Lee-Carter) :** Projection stochastique de l'espérance de vie.
*   **Assurance Vie Luxembourg :** Spécificités (Triangle de sécurité, FID/FAS).
*   **SCR Lux (Réassurance) :** Modèle de filiale réassurée à 100%.
*   **Provisionnement (Chain-Ladder) :** Estimation des IBNR Non-Vie.
*   **Pilotage Réassurance :** Optimisation de la structure XL.
*   **SCR Global :** Agrégation des risques et matrice de corrélation.

## 🚀 Installation et Lancement

### Pré-requis
*   Python 3.10 ou supérieur

### Installation des dépendances
```bash
pip install -r requirements.txt
```

### Lancement de l'application
```bash
streamlit run Accueil.py
```

## 🛠 Bibliothèques Principales

*   `streamlit` : Framework Web UI.
*   `plotly` : Visualisations interactives.
*   `numpy` / `pandas` : Calcul matriciel et manipulation de données.
*   `scipy` : Optimisation (Calibration Nelson-Siegel).
*   `chainladder` : Algorithmes de provisionnement.
*   `smithwilson` : Moteur d'extrapolation des taux.

---
*Ce projet a été développé dans un but pédagogique et de démonstration professionnelle.*