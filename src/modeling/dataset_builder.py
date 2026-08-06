import numpy as np
import pandas as pd

def build_feature_matrix(lst, albedo, net_rad, ndvi, ndbi, ndmi, ndvi_mean, albedo_mean, true_svf, z0, dist_water, dist_veg, c_g, bsi, fvc, pai, pop, road_density, ghsl_built):
    features = {
        'LST_Celsius': lst.flatten(),
        'Albedo_Liang_S2': albedo.flatten(),
        'NDVI_Greenness': ndvi.flatten(),
        'NDMI_Moisture': ndmi.flatten(),
        'BSI_Bare_Soil': bsi.flatten(),
        'FVC_Veg_Cover': fvc.flatten(),
        'Population_Density_GHSL': pop.flatten(),
        'GHSL_Built_Surface': ghsl_built.flatten(),
        'NDVI_Neighborhood_Mean': ndvi_mean.flatten(),
        'Albedo_Neighborhood_Mean': albedo_mean.flatten(),
        'Exponential_Decay_Water': dist_water.flatten(),
        'Exponential_Decay_Veg': dist_veg.flatten(),
        'Thermal_Admittance_cG': c_g.flatten()
    }
    return pd.DataFrame(features)
