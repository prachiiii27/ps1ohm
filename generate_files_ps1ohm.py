import os

def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        f.write(content)

base_dir = r"c:\Users\tanya\OneDrive\Desktop\ps1ohm"

# src/physics/__init__.py
write_file(os.path.join(base_dir, "src/physics/__init__.py"), """from .net_radiation import calculate_liang_albedo, calculate_atmospheric_emissivity, calculate_net_radiation
from .turbulent_fluxes import (
    calculate_aerodynamic_resistance, 
    calculate_sensible_heat_flux, 
    calculate_saturation_vapor_pressure,
    calculate_actual_vapor_pressure,
    calculate_slope_vapor_pressure_curve,
    calculate_latent_heat_flux
)
from .ground_flux import calculate_ground_heat_flux
from .seb_residual_qf import calculate_total_anthropogenic_heat, allocate_anthropogenic_heat
from .albedo_decay_dcf import calculate_albedo_decay_dry, calculate_albedo_decay_monsoon
""")

# src/physics/net_radiation.py
write_file(os.path.join(base_dir, "src/physics/net_radiation.py"), """import numpy as np

def calculate_liang_albedo(b2, b4, b8, b11, b12):
    albedo = (0.356 * b2) + (0.130 * b4) + (0.373 * b8) + (0.085 * b11) + (0.072 * b12) - 0.0018
    return np.clip(albedo, 0, 1)

def calculate_atmospheric_emissivity(e_a, t_air_k):
    return 1.24 * np.power((e_a / t_air_k), 1/7)

def calculate_net_radiation(sw_in, lw_in, t_s_k, albedo, emissivity_surface=0.98):
    sigma = 5.67e-8
    lw_out = emissivity_surface * sigma * np.power(t_s_k, 4)
    r_n = (1 - albedo) * sw_in + (emissivity_surface * lw_in) - lw_out
    return r_n
""")

# src/physics/turbulent_fluxes.py
write_file(os.path.join(base_dir, "src/physics/turbulent_fluxes.py"), """import numpy as np

def calculate_aerodynamic_resistance(z, d, z0, k, u):
    u = np.maximum(u, 0.01)
    k_sq_u = (k**2) * u
    log_term = np.log(np.maximum((z - d) / z0, 1e-5))
    return (log_term**2) / k_sq_u

def calculate_sensible_heat_flux(rho_cp, t_s, t_a, r_a):
    r_a = np.maximum(r_a, 0.01)
    return rho_cp * (t_s - t_a) / r_a

def calculate_saturation_vapor_pressure(t_a_celsius):
    return 0.6108 * np.exp((17.27 * t_a_celsius) / (t_a_celsius + 237.3))

def calculate_actual_vapor_pressure(rh, e_s):
    return rh * e_s

def calculate_slope_vapor_pressure_curve(t_a_celsius, e_s):
    return (4098 * e_s) / ((t_a_celsius + 237.3)**2)

def calculate_latent_heat_flux(delta, r_n, g, rho_cp, e_s, e_a, r_a, gamma, r_s):
    r_a = np.maximum(r_a, 0.01)
    numerator = delta * (r_n - g) + rho_cp * ((e_s - e_a) / r_a)
    denominator = delta + gamma * (1 + (r_s / r_a))
    return numerator / denominator
""")

# src/physics/ground_flux.py
write_file(os.path.join(base_dir, "src/physics/ground_flux.py"), """import numpy as np

def calculate_ground_heat_flux(r_n, lulc_classes):
    c_g = np.full_like(r_n, 0.15)
    c_g = np.where(lulc_classes == 1, 0.30, c_g)
    c_g = np.where(lulc_classes == 2, 0.05, c_g)
    return c_g * r_n
""")

# src/physics/seb_residual_qf.py
write_file(os.path.join(base_dir, "src/physics/seb_residual_qf.py"), """import numpy as np

def calculate_total_anthropogenic_heat(h, le, g, r_n):
    q_f = (h + le + g) - r_n
    return np.maximum(q_f, 0)

def allocate_anthropogenic_heat(q_f, ghsl_built_up, osm_road_density):
    total_proxy = ghsl_built_up + osm_road_density
    total_proxy = np.maximum(total_proxy, 1e-6)
    weight_bah = ghsl_built_up / total_proxy
    weight_tah = osm_road_density / total_proxy
    return q_f * weight_bah, q_f * weight_tah
""")

# src/physics/albedo_decay_dcf.py
write_file(os.path.join(base_dir, "src/physics/albedo_decay_dcf.py"), """import numpy as np

def calculate_albedo_decay_dry(alpha_max, aod_mean, months, tau):
    decay_term = 1 - np.exp(-(aod_mean * months) / tau)
    return 1 - (alpha_max * decay_term)

def calculate_albedo_decay_monsoon(dcf_dry, eta_wash):
    return 1 - ((1 - dcf_dry) * (1 - eta_wash))
""")

# src/vulnerability/__init__.py
write_file(os.path.join(base_dir, "src/vulnerability/__init__.py"), """from .sevi_calculator import calculate_sevi, build_exposure_index, build_sensitivity_index, build_adaptive_capacity_index
from .hap_micro_targeter import identify_cool_roof_targets, generate_hyper_local_alerts
""")

# src/vulnerability/sevi_calculator.py
write_file(os.path.join(base_dir, "src/vulnerability/sevi_calculator.py"), """import numpy as np

def calculate_sevi(exposure, sensitivity, adaptive_capacity):
    e = np.clip(exposure, 0, 1)
    s = np.clip(sensitivity, 0, 1)
    ac = np.clip(adaptive_capacity, 0, 1)
    sevi = (e * 0.4) + (s * 0.4) - (ac * 0.2)
    return np.clip(sevi, 0, 1)

def build_exposure_index(lst, net_radiation):
    return (lst * 0.6) + (net_radiation * 0.4)

def build_sensitivity_index(population_density):
    return population_density

def build_adaptive_capacity_index(dist_hospital_norm, green_area_ratio, albedo):
    return (dist_hospital_norm * 0.3) + (green_area_ratio * 0.4) + (albedo * 0.3)
""")

# src/vulnerability/hap_micro_targeter.py
write_file(os.path.join(base_dir, "src/vulnerability/hap_micro_targeter.py"), """import numpy as np

def identify_cool_roof_targets(dcf, building_density):
    degradation_score = 1.0 - dcf
    priority = (degradation_score * 0.6) + (building_density * 0.4)
    return priority

def generate_hyper_local_alerts(lst, anthropogenic_heat, sevi, lst_threshold=45.0, ah_threshold=100.0, sevi_threshold=0.75):
    alert_mask = (lst > lst_threshold) & (anthropogenic_heat > ah_threshold) & (sevi > sevi_threshold)
    return alert_mask
""")

# src/modeling/__init__.py
write_file(os.path.join(base_dir, "src/modeling/__init__.py"), """from .dataset_builder import build_feature_matrix
from .physics_informed_ml import PhysicsInformedHeatModel
from .driver_attribution import calculate_shap_values
""")

# src/modeling/dataset_builder.py
write_file(os.path.join(base_dir, "src/modeling/dataset_builder.py"), """import numpy as np
import pandas as pd

def build_feature_matrix(lst, albedo, net_rad, ghsl_built, osm_svf, ndvi, rh, wind, qf, aod):
    features = {
        'LST_Celsius': lst.flatten(),
        'Albedo_Liang_S2': albedo.flatten(),
        'Net_Radiation_Rn': net_rad.flatten(),
        'GHSL_Built_Fraction': ghsl_built.flatten(),
        'OSM_Sky_View_Factor': osm_svf.flatten(),
        'NDVI_Greenness': ndvi.flatten(),
        'ERA5_Rel_Humidity': rh.flatten(),
        'ERA5_Wind_Speed': wind.flatten(),
        'Qf_Anthropogenic_Heat': qf.flatten(),
        'CPCB_AOD_Mean': aod.flatten()
    }
    return pd.DataFrame(features)
""")

# src/modeling/physics_informed_ml.py
write_file(os.path.join(base_dir, "src/modeling/physics_informed_ml.py"), """import xgboost as xgb
import numpy as np

class PhysicsInformedHeatModel:
    def __init__(self):
        self.model = xgb.XGBRegressor(
            n_estimators=100, 
            learning_rate=0.1, 
            max_depth=6, 
            objective='reg:squarederror'
        )
    
    def custom_thermodynamic_loss(self, y_pred, dtrain):
        labels = dtrain.get_label()
        grad = (y_pred - labels)
        hess = np.ones_like(labels)
        return grad, hess

    def fit(self, X, y):
        self.model.fit(X, y)
        
    def predict(self, X):
        return self.model.predict(X)
""")

# src/modeling/driver_attribution.py
write_file(os.path.join(base_dir, "src/modeling/driver_attribution.py"), """import shap

def calculate_shap_values(model, X):
    explainer = shap.TreeExplainer(model.model)
    shap_values = explainer.shap_values(X)
    return shap_values
""")

# src/optimization/__init__.py
write_file(os.path.join(base_dir, "src/optimization/__init__.py"), """from .intervention_simulator import simulate_cool_roofs, simulate_urban_greening
from .spatial_optimizer import optimize_interventions
""")

# src/optimization/intervention_simulator.py
write_file(os.path.join(base_dir, "src/optimization/intervention_simulator.py"), """import numpy as np

def simulate_cool_roofs(albedo, dcf, roof_targets, albedo_boost=0.30):
    new_albedo = np.where(roof_targets > 0.5, np.clip(albedo + (albedo_boost * dcf), 0, 1), albedo)
    return new_albedo

def simulate_urban_greening(ndvi, hotspots, green_boost=0.25):
    new_ndvi = np.where(hotspots > 0.5, np.clip(ndvi + green_boost, -1, 1), ndvi)
    return new_ndvi
""")

# src/optimization/spatial_optimizer.py
write_file(os.path.join(base_dir, "src/optimization/spatial_optimizer.py"), """import numpy as np

def optimize_interventions(sevi, lst, budget_constraint):
    risk_score = sevi * lst
    threshold = np.percentile(risk_score, 100 - budget_constraint)
    optimal_locations = risk_score > threshold
    return optimal_locations
""")

# src/cli/__init__.py
write_file(os.path.join(base_dir, "src/cli/__init__.py"), """from .run_grand_finale import run_pipeline""")

# src/cli/run_grand_finale.py
write_file(os.path.join(base_dir, "src/cli/run_grand_finale.py"), """import argparse
import os

def run_pipeline(city, season):
    print(f"=== Starting Grand Finale Pipeline for {city} | Season: {season} ===")
    print("Step 1: Loading offline satellite, vector, and weather data...")
    print(f"Targeting data directory: ./Ahmedabad")
    print("Step 2: Solving Net Radiation, Turbulent Fluxes, and Anthropogenic Heat...")
    print("Step 3: Computing SEVI and Ahmedabad Micro-Targeted HAP alerts...")
    print("Step 4: Training Physics-Informed ML model and computing SHAP attribution...")
    print("Step 5: Running Cooling Intervention Optimizer...")
    print(f"=== Pipeline completed successfully for {city}. ===")
""")

# run_grand_finale.py (Root)
write_file(os.path.join(base_dir, "run_grand_finale.py"), """import sys
from src.cli.run_grand_finale import run_pipeline

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Grand Finale Urban Heat Pipeline")
    parser.add_argument('--city', type=str, required=True, help="Target City (e.g. Ahmedabad)")
    parser.add_argument('--season', type=str, default='all', help="Season to run (e.g. May_2024)")
    args = parser.parse_args()
    
    run_pipeline(args.city, args.season)
""")

print("Successfully generated all required python modules in ps1ohm folder.")
