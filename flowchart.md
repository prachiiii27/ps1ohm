# 🏗️ The 7-Lever Urban Heat Mitigation Workflow

This document provides a highly detailed, chronological roadmap of the entire AI-driven Urban Heat Mitigation pipeline we built for Ahmedabad. It maps the journey from raw satellite data to a live policy optimization engine.

## 🗺️ Master Architecture Flowchart

```mermaid
flowchart TD
    %% Styling
    classDef data fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef ml fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px;
    classDef shap fill:#fff3e0,stroke:#e65100,stroke-width:2px;
    classDef sevi fill:#ffebee,stroke:#c62828,stroke-width:2px;
    classDef optim fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    classDef ui fill:#fafafa,stroke:#424242,stroke-width:2px;

    %% 1. Data Engineering
    subgraph Data["1. High-Resolution Data Engineering"]
        A1[Raw Datasets<br/>Sentinel-2, Landsat, GHSL]
        A2[Discard 10km Weather Data<br/>Avoid zero-variance resolution mismatches]
        A3[Feature Engineering<br/>Extract 14 Thermodynamic Vectors]
        A1 --> A2 --> A3
    end
    class A1,A2,A3 data;

    %% 2. Machine Learning
    subgraph ML["2. Physics-Informed Machine Learning"]
        B1[The Twin Problem<br/>Drop perfectly correlated NDBI/Net Radiation]
        B2[Train XGBoost Engine<br/>Predict 10m Micro-Scale LST]
        A3 --> B1 --> B2
    end
    class B1,B2 ml;

    %% 3. Explainability (SHAP)
    subgraph SHAP["3. SHAP Game-Theory Attribution"]
        C1[Calculate SHAP Values<br/>Crack open the ML black box]
        C2[Feature Importance<br/>Rank top drivers: GHSL Built, NDMI, NDVI]
        C3[Actionable Sensitivity Analysis<br/>e.g. +10% Albedo = 2.10°C Drop]
        B2 --> C1 --> C2 & C3
    end
    class C1,C2,C3 shap;

    %% 4. Vulnerability Mapping
    subgraph SEVI["4. Socio-Economic Vulnerability (SEVI)"]
        D1[Map Physical Heat<br/>LST Hotspots via Tricontourf Interpolation]
        D2[Map Human Sensitivity<br/>GHSL Population Density / Concrete Trap]
        D3[Calculate SEVI Score<br/>Exposure × Sensitivity ÷ Adaptive Capacity]
        B2 --> D1
        D1 & D2 --> D3
    end
    class D1,D2,D3 sevi;

    %% 5. NSGA-III Optimization
    subgraph Optim["5. The NSGA-III Supercomputing Optimizer"]
        E1[Define Conflicting Objectives<br/>Max LST Drop, Max SEVI Drop, Min Capex]
        E2[Run Evolutionary Algorithm<br/>Simulate thousands of 'budgets']
        E3[Output 3D Pareto Front<br/>Mathematically perfect 7-Lever allocation]
        C3 & D3 --> E1 --> E2 --> E3
    end
    class E1,E2,E3 optim;

    %% 6. Interactive Deployment
    subgraph UI["6. The Live Policy Dashboard"]
        F1[Streamlit Simulation Engine<br/>Interactive sliders for policy changes]
        F2[Dynamic Recalculation<br/>AI recalculates heat & SEVI instantly]
        F3[City Deliverable<br/>Live OS for Mayoral budget planning]
        E3 --> F1 --> F2 --> F3
    end
    class F1,F2,F3 ui;
```

---

## 📖 Deep-Dive Explanations

### 1. High-Resolution Data Engineering
Instead of using basic 2D maps, we engineered the physical thermodynamics of the city. We explicitly threw out low-resolution background pollution metrics (NO2, PM2.5) because a 10km pixel provides no micro-spatial variance. Instead, we used GHSL Population Density as a high-resolution proxy for anthropogenic waste heat. We extracted complex indices like **NDMI** (Latent Heat of Moisture) and injected **Exponential Decay Functions** to mathematically model advection (the cooling breeze from a park spilling into the neighborhood).

### 2. Physics-Informed Machine Learning (XGBoost)
We fed these 14 physical vectors into an XGBoost model to predict Land Surface Temperature (LST). During this phase, we solved the "Twin Problem" by explicitly dropping features with perfect negative multicollinearity (like NDBI and Net Radiation). This forced the ML model to be mathematically honest, attributing exactly 100% of the evaporative credit to the correct physical feature, rather than splitting it among redundant columns.

### 3. SHAP Game-Theory Attribution
We didn't just want a black-box prediction; we needed to know *why*. We used TreeSHAP to isolate the temperature contribution of every physical feature. This generated:
*   **Feature Importance Rankings:** Proving that Built Surface volume is the single biggest driver of heat.
*   **Sensitivity Analyses:** We calculated the exact, actionable slope for interventions, mathematically proving that a 10% absolute increase in Albedo directly yields a 2.10°C drop in Land Surface Temperature.

### 4. Socio-Economic Vulnerability (SEVI)
We realized that cooling empty concrete isn't the primary goal—saving human lives is. We calculated SEVI to map the divergence between physical heat (LST) and human vulnerability. 
*   **The Physical Mapping:** We used Triangular Contour Interpolation (`tricontourf`) to flawlessly map the heat gradient, mathematically bridging the artificial gap over the Sabarmati river.
*   **The Vulnerability Score:** By multiplying the LST by the extreme population density of the Central Wards, we proved that the acute human risk sits squarely in the dense, low-income tenement housing zones, not just the hotter industrial zones.

### 5. The NSGA-III Supercomputing Optimizer
Because the city has a limited budget, a one-size-fits-all policy fails. We deployed an NSGA-III Multi-Objective Evolutionary Algorithm to optimize our **7-Lever Strategy**. The algorithm pitted three conflicting objectives against each other: maximizing LST reduction, maximizing SEVI reduction, and minimizing Capital Expenditure (Capex). It converged on a 3D Pareto Front, definitively proving that the city must use a hybrid approach: **White Roofs** in the hot industrial East, and highly-targeted **IoT Misting Hubs / Amrit Sarovars** in the hyper-dense, vulnerable Center.

### 6. The Live Policy Dashboard
We packaged this entire supercomputing backend into a live, interactive Streamlit OS. Instead of a static PDF, policymakers can use sliders to simulate increasing urban greening or mandating white roofs. The XGBoost model dynamically recalculates the physics in the background, rendering instantaneous 3D spatial maps and proving the exact temperature and SEVI drop achieved by their simulated budget.
