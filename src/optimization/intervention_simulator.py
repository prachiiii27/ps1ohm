import numpy as np

def simulate_cool_roofs(albedo, dcf, roof_targets, albedo_boost=0.30):
    new_albedo = np.where(roof_targets > 0.5, np.clip(albedo + (albedo_boost * dcf), 0, 1), albedo)
    return new_albedo

def simulate_urban_greening(ndvi, hotspots, green_boost=0.25):
    new_ndvi = np.where(hotspots > 0.5, np.clip(ndvi + green_boost, -1, 1), ndvi)
    return new_ndvi
