import numpy as np

def calculate_total_anthropogenic_heat(h, le, g, r_n):
    q_f = (h + le + g) - r_n
    return np.maximum(q_f, 0)

def allocate_anthropogenic_heat(q_f, ghsl_built_up, osm_road_density):
    total_proxy = ghsl_built_up + osm_road_density
    total_proxy = np.maximum(total_proxy, 1e-6)
    weight_bah = ghsl_built_up / total_proxy
    weight_tah = osm_road_density / total_proxy
    return q_f * weight_bah, q_f * weight_tah
