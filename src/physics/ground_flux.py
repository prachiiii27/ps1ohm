import numpy as np

def calculate_ground_heat_flux(r_n, lulc_classes):
    """
    Calculates Ground Heat Flux (G = c_G * R_n) based on 4 LULC classes:
    1 = Buildup (c_G = 0.30)
    2 = Vegetation (c_G = 0.05)
    3 = Water Bodies (c_G = 0.50)
    4 = Barren Land (c_G = 0.15)
    """
    # Initialize c_G array with zeros
    c_g = np.zeros_like(r_n)
    
    # Map the 4 classes to their respective c_G constants
    c_g = np.where(lulc_classes == 1, 0.30, c_g)  # Buildup
    c_g = np.where(lulc_classes == 2, 0.05, c_g)  # Vegetation
    c_g = np.where(lulc_classes == 3, 0.50, c_g)  # Water Bodies
    c_g = np.where(lulc_classes == 4, 0.15, c_g)  # Barren Land
    
    return c_g * r_n
