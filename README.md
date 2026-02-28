# 📊 Portfolio Actuariat & Data Science

**Auteur :** Nicolas Rivollet  
**Stack :** Python, Streamlit, Plotly, NumPy, Pandas

## 🎯 Objectif du Projet

Ce projet est une application web interactive démontrant l'application de techniques de **Data Science** et de **développement logiciel** aux problématiques actuarielles modernes.

Il sert de support de démonstration pour des compétences en :
*   **Modélisation Financière :** Courbes de taux (Nelson-Siegel, Smith-Wilson).
*   **Solvabilité II :** Calculs de SCR, Marge de Risque, Volatility Adjustment.
*   **Assurance Vie :** Modélisation de la mortalité (Lee-Carter).
*   **Assurance Non-Vie :** Provisionnement (Chain-Ladder) et Cartographie des risques (Cat Nat).

## 🗂 Structure de l'Application

L'application est structurée en modules thématiques accessibles via une barre de navigation latérale :

### 1. Finance & ALM
*   **Modèle Nelson-Siegel :** Calibration et simulation de la courbe des taux.
*   **Modèle Smith-Wilson :** Extrapolation réglementaire (EIOPA).
*   **Pilotage Réassurance :** Optimisation de la structure XL via simulation Monte Carlo.

### 2. Réglementation & ESG
*   **Architecture S2 :** Explorateur interactif des textes (Directive vs Règlement Délégué).
*   **SCR Standard :** Agrégation des risques et matrice de corrélation.
*   **SCR Taux :** Calcul du choc de taux (Up/Down) sur la NAV.
*   **Volatility Adjustment :** Simulation de l'impact sur le bilan.
*   **Risque Climatique :** Cartographie des impacts Cat Nat (Scénarios GIEC).

### 3. Assurance Vie & Non-Vie
*   **Mortalité (Lee-Carter) :** Projection stochastique de l'espérance de vie.
*   **Provisionnement (Chain-Ladder) :** Estimation des IBNR et triangle de liquidation.

## 🚀 Installation et Lancement

### Pré-requis
*   Python 3.8 ou supérieur

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