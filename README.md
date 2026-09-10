# Urban Heat Action Plan (UHAP) — Decision Support System 🌡️🏙️

> **Team: Flux Fixers | IIT Gandhinagar — Problem Statement 1 (PS-1)**

A data-driven, machine learning-powered **Decision Support System (DSS)** designed for municipal administrators and urban planners to prioritize, model, and deploy heat mitigation interventions across Ahmedabad's wards.

---

## 🎯 Problem Context

Urban Heat Islands (UHIs) cause severe heat stress in densely populated cities, disproportionately impacting vulnerable communities. This platform bridges satellite data, socio-economic demographics, and machine learning to deliver actionable, ward-specific intervention roadmaps.

---

## 🗂️ Repository Structure

```
ps1ohm/
├── app.py                          # Streamlit Interactive Web Application (Dashboard)
├── ds_dashboard.py                 # Data Science and analytics dashboard modules
├── train_model.py                  # XGBoost model training & performance evaluation
├── tune_hyperparams.py             # Hyperparameter tuning routines
├── execute_pipeline.py             # End-to-end data processing and model pipeline
├── generate_city_maps.py           # Geospatial PyDeck/Folium ward map generators
├── generate_shap_analysis.py       # SHAP explainability & feature attribution
├── generate_sensitivity_metrics.py # Sensitivity analysis across intervention types
├── update_ward_summary.py          # Summary metrics generation per ward
├── run_grand_finale.py             # Final evaluation and report aggregation
├── flowchart.md                    # Architecture & pipeline diagrams
├── sevi_nsga3_flowchart.md         # Multi-objective NSGA-III optimization logic
├── model_training_data.csv         # Ward-level training dataset
├── Ahmedabad/                      # Ward boundary shapefiles & GeoJSON data
├── data/                           # Processed heat index and demographic inputs
├── deliverables/                   # Generated reports and executive summaries
├── invest_model/                   # Cost-benefit models and budget allocations
├── shap_analysis/                  # Summary plots, dependence plots, waterfall charts
└── src/                            # Modular utility functions and calculation scripts
```

---

## 🧠 System Pipeline

```
[ Satellite LST + NDVI + Demographics ]
                   │
                   ▼
  [ XGBoost Vulnerability Predictor ]
                   │
                   ▼
[ SHAP Feature Importance Explainer ]
                   │
                   ▼
 [ NSGA-III Multi-Objective Optimizer ]
   (Min Cost | Max Cooling | Max Equity)
                   │
                   ▼
[ Interactive Streamlit 3D Dashboard ]
```

---

## 🚀 Quickstart Guide

### 1. Install Dependencies
```bash
pip install streamlit pandas numpy pydeck scikit-learn xgboost shap pymoo plotly
```

### 2. Launch the Decision Support Dashboard
```bash
streamlit run app.py
```

### 3. Run the Full ML Pipeline
```bash
python execute_pipeline.py
```

---

## 🌟 Key Features

- **3D Interactive Ward Maps:** Visualise Land Surface Temperature (LST), Green Cover, and Socio-Economic Vulnerability Index (SEVI).
- **Multi-Objective Optimization (NSGA-III):** Balance municipal budget limits against maximum temperature reduction and social equity.
- **Explainable AI (XAI):** SHAP analysis detailing why specific wards are at severe risk.
- **Custom Policy Simulations:** Test intervention scenarios (cool roofs, urban greening, misting stations) with real-time impact estimations.

---

## 📄 Key Documentation

- [`Idea_Submission_Flux_Fixers(PS1).pdf`](Idea_Submission_Flux_Fixers(PS1).pdf) — Problem Statement 1 Idea Proposal
- [`flowchart.md`](flowchart.md) — End-to-end technical system architecture
- [`sevi_nsga3_flowchart.md`](sevi_nsga3_flowchart.md) — Multi-objective algorithm design

---

## 👤 Author

**Prachi Jindal**  
Junior Undergraduate, Mechanical Engineering  
Indian Institute of Technology Gandhinagar (IITGN)
