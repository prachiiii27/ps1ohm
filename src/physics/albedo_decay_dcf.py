import numpy as np

def calculate_albedo_decay_dry(alpha_max, aod_mean, months, tau):
    decay_term = 1 - np.exp(-(aod_mean * months) / tau)
    return 1 - (alpha_max * decay_term)
