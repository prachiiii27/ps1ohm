# 🧬 Deep-Dive Architecture: SEVI & NSGA-III Optimizer

This document provides a highly magnified look at the two most critical public policy engines in the Ahmedabad Urban Heat pipeline: The **Socio-Economic Vulnerability Index (SEVI)** and the **NSGA-III Evolutionary Optimizer**.

## 🗺️ The Optimization Flowchart

```mermaid
flowchart TD
    %% Styling
    classDef input fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef math fill:#fff3e0,stroke:#e65100,stroke-width:2px;
    classDef output fill:#ffebee,stroke:#c62828,stroke-width:2px;
    classDef nsga fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    classDef pareto fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px;

    %% -----------------------------------------------------
    %% Phase 1: SEVI Calculation
    %% -----------------------------------------------------
    subgraph SEVI_Engine["Phase 1: Humanizing the Heat (SEVI Calculation)"]
        
        I1[Exposure<br/>Predicted LST Excess]
        I2[Sensitivity<br/>GHSL Population Density & Concrete Volume]
        I3[Adaptive Capacity<br/>Green Ratio & Reflectivity]
        
        Math_SEVI{"SEVI Formula<br/>(Exposure × Sensitivity)<br/>÷ Adaptive Capacity"}
        
        O1[Vulnerability Output<br/>Hyper-Localized SEVI Hotspot Map]
        
        I1 --> Math_SEVI
        I2 --> Math_SEVI
        I3 --> Math_SEVI
        Math_SEVI --> O1
    end
    class I1,I2,I3 input;
    class Math_SEVI math;
    class O1 output;

    %% -----------------------------------------------------
    %% Phase 2: NSGA-III Optimization
    %% -----------------------------------------------------
    subgraph NSGA_Engine["Phase 2: The Evolutionary Policy Optimizer (NSGA-III)"]
        
        N1((Initialize NSGA-III))
        
        Obj1[Objective 1<br/>Maximize SEVI Reduction]
        Obj2[Objective 2<br/>Maximize LST Reduction]
        Obj3[Objective 3<br/>Minimize Capital Expenditure]
        
        Evolution[Evolutionary Cycle<br/>Mutate 7-Lever allocation budgets across 40 Generations]
        
        Pareto[Final Output<br/>Mathematically Perfect 3D Pareto Front]
        
        O1 --> N1
        N1 --> Obj1 & Obj2 & Obj3
        Obj1 & Obj2 & Obj3 --> Evolution
        Evolution --> Pareto
    end
    class N1,Evolution nsga;
    class Obj1,Obj2,Obj3 math;
    class Pareto pareto;

    %% Connecting the phases
    O1 ===>|Feeds Vulnerability Data| N1
```

---

## 🔬 Component Breakdown

### Phase 1: SEVI (Socio-Economic Vulnerability Index)
The SEVI engine ensures the city isn't just cooling empty concrete, but actually saving lives. It mathematically intersects three physical realities:
1.  **Exposure:** Supplied directly by our XGBoost engine, this is the actual physical heat signature (LST Excess) of a 10m grid.
2.  **Sensitivity:** We use GHSL Population Density as a physical proxy for human bodies. If 1,000 people are trapped in a dense concrete grid, their thermodynamic sensitivity is mathematically scaled up due to extreme density and anthropogenic waste heat.
3.  **Adaptive Capacity:** This acts as the mathematical denominator. If a grid has high greenery or cooling infrastructure, the vulnerability is divided (reduced). 
*Result:* The engine outputs a heat map proving that human vulnerability peaks in the dense, central slums (e.g., Danilimda), not the absolute hottest industrial zones.

### Phase 2: NSGA-III (Non-dominated Sorting Genetic Algorithm III)
Policy making is a game of scarce resources. The NSGA-III algorithm is a supercomputing architecture that acts like natural selection to find the perfect budget allocation.
1.  **The Inputs:** It ingests the LST map and the SEVI map.
2.  **The Conflicting Objectives:** It tries to cool the city (Drop LST), save the humans (Drop SEVI), and save money (Minimize Capex) all at the exact same time. These three goals inherently conflict with each other.
3.  **The Evolution:** Over 40 generations, the AI mutates thousands of simulated "budgets" (e.g., testing what happens if it spends ₹50 Lakh on White Roofs in Vatva vs. IoT Misting in Gomtipur).
4.  **The 3D Pareto Front:** It converges on the absolute mathematically optimal strategy—a 3D curve where it is impossible to gain even 0.1°C more cooling without spending more money. This mathematically proves that a hybrid 7-Lever strategy is superior to a blanket one-size-fits-all policy.
