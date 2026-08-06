import numpy as np
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.optimize import minimize
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.repair.rounding import RoundingRepair
import warnings

warnings.filterwarnings("ignore")

class UrbanCoolingProblem(ElementwiseProblem):
    """
    NSGA-III Multi-Objective Genetic Algorithm Problem for Urban Cooling.
    Optimizes the allocation of interventions across N highest-risk zones.
    
    Decisions per zone:
    0: Do nothing
    1: Apply Cool Roof Mandate
    2: Apply Urban Greening
    
    Objectives:
    f1: Minimize remaining SEVI (Protect Vulnerable Populations)
    f2: Minimize Population-Weighted LST (Maximize Cooling Impact)
    f3: Minimize Capital Expenditure (Financial Constraint)
    """
    def __init__(self, n_zones, base_sevi, base_lst, pop_density, 
                 cost_cool_roof=5000, cost_greening=12000, 
                 sevi_reduction_roof=0.1, sevi_reduction_green=0.15,
                 lst_reduction_roof=1.5, lst_reduction_green=2.0):
                 
        self.n_zones = n_zones
        self.base_sevi = base_sevi
        self.base_lst = base_lst
        self.pop_density = pop_density
        
        self.cost_cool_roof = cost_cool_roof
        self.cost_greening = cost_greening
        self.sevi_reduction_roof = sevi_reduction_roof
        self.sevi_reduction_green = sevi_reduction_green
        self.lst_reduction_roof = lst_reduction_roof
        self.lst_reduction_green = lst_reduction_green
        
        # 3 objectives, n_zones decision variables (each bounded 0 to 2)
        super().__init__(n_vars=self.n_zones, n_obj=3, n_ieq_constr=0, xl=0, xu=2)

    def _evaluate(self, x, out, *args, **kwargs):
        # x is an array of size n_zones with integer values {0, 1, 2}
        total_sevi = 0.0
        total_pop_lst = 0.0
        total_capex = 0.0
        
        for i in range(self.n_zones):
            decision = int(np.round(x[i]))
            
            sevi_val = self.base_sevi[i]
            lst_val = self.base_lst[i]
            pop = self.pop_density[i]
            
            if decision == 1: # Cool Roof
                sevi_val = max(0, sevi_val - self.sevi_reduction_roof)
                lst_val = max(0, lst_val - self.lst_reduction_roof)
                total_capex += self.cost_cool_roof
            elif decision == 2: # Greening
                sevi_val = max(0, sevi_val - self.sevi_reduction_green)
                lst_val = max(0, lst_val - self.lst_reduction_green)
                total_capex += self.cost_greening
                
            total_sevi += sevi_val
            total_pop_lst += (lst_val * pop)
            
        out["F"] = [total_sevi, total_pop_lst, total_capex]

def run_nsga3_optimization(sevi_map, lst_map, pop_map, n_zones=100, generations=40):
    """
    Executes the NSGA-III Genetic Algorithm on the top N most vulnerable clusters.
    """
    print(f"--- Launching NSGA-III Evolutionary Engine on Top {n_zones} High-Risk Zones ---")
    
    # 1. Flatten and identify the highest risk zones (to keep computation viable)
    risk_score = sevi_map * lst_map
    flat_indices = np.argsort(risk_score.flatten())[::-1][:n_zones]
    
    base_sevi = sevi_map.flatten()[flat_indices]
    base_lst = lst_map.flatten()[flat_indices]
    pop_density = pop_map.flatten()[flat_indices]
    
    # 2. Define the Problem
    problem = UrbanCoolingProblem(n_zones, base_sevi, base_lst, pop_density)
    
    # 3. Setup NSGA-III Reference Directions (Standard for 3+ objectives)
    ref_dirs = get_reference_directions("das-dennis", 3, n_partitions=12)
    
    algorithm = NSGA3(
        pop_size=len(ref_dirs) + 10,
        ref_dirs=ref_dirs,
        sampling=IntegerRandomSampling(),
        crossover=SBX(prob=1.0, eta=3.0, vtype=float, repair=RoundingRepair()),
        mutation=PM(prob=1.0/n_zones, eta=3.0, vtype=float, repair=RoundingRepair()),
        eliminate_duplicates=True
    )
    
    # 4. Execute Evolutionary Process
    res = minimize(
        problem,
        algorithm,
        ("n_gen", generations),
        seed=42,
        verbose=False
    )
    
    print(f"-> NSGA-III successfully evolved {len(res.F)} optimal Pareto front solutions!")
    return res.X, res.F, flat_indices
