import numpy as np
from .nsga3_optimizer import run_nsga3_optimization

def optimize_interventions_legacy(sevi, lst, budget_constraint):
    """
    Deprecated basic thresholding function.
    """
    risk_score = sevi * lst
    threshold = np.percentile(risk_score, 100 - budget_constraint)
    optimal_locations = risk_score > threshold
    return optimal_locations

def optimize_interventions_nsga3(sevi_map, lst_map, pop_map, n_zones=100, generations=40):
    """
    Executes the advanced Multi-Objective NSGA-III Evolutionary algorithm.
    Returns:
    - X_pareto: The matrix of intervention decisions across the Pareto front.
    - F_pareto: The 3D objective scores (SEVI, LST, Capex) for each scenario.
    - target_indices: The flat array indices of the targeted high-risk zones.
    """
    X_pareto, F_pareto, target_indices = run_nsga3_optimization(
        sevi_map=sevi_map, 
        lst_map=lst_map, 
        pop_map=pop_map, 
        n_zones=n_zones, 
        generations=generations
    )
    return X_pareto, F_pareto, target_indices
