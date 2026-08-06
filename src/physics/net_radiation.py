import numpy as np

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
