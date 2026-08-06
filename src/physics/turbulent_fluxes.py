import numpy as np

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
