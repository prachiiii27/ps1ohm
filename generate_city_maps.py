import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

out_dir = "deliverables"
os.makedirs(out_dir, exist_ok=True)

print("Loading 100m grid data...")
df = pd.read_parquet("data/ahmedabad_grid_100m.parquet")

# 1. Urban Heat Island (UHI) Map (Optimized Lower Resolution Hexbin)
print("Generating Urban Heat Island (UHI) Map...")
plt.figure(figsize=(12, 10))
# Using hexbin to decrease resolution and create a smooth spatial heat map
hb1 = plt.hexbin(df['lon'], df['lat'], C=df['lst_excess'], gridsize=60, cmap='jet', reduce_C_function=np.mean, edgecolors='none', alpha=0.9)
plt.colorbar(hb1, label='UHI Intensity / LST Excess (°C)')
plt.title('Ahmedabad City: Urban Heat Island (UHI) Intensity', fontsize=16)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.tight_layout()
plt.savefig(os.path.join(out_dir, "Ahmedabad_Urban_Heat_Island_Map.png"), dpi=300, bbox_inches='tight')
plt.close()

# 2. SEVI (Heat Stress) Map (Optimized Lower Resolution Hexbin)
print("Generating Heat Stress (SEVI) Map...")
plt.figure(figsize=(12, 10))
# Using hexbin to decrease resolution and create a smooth spatial heat map
hb2 = plt.hexbin(df['lon'], df['lat'], C=df['sevi'], gridsize=60, cmap='YlOrRd', reduce_C_function=np.mean, edgecolors='none', alpha=0.9)
plt.colorbar(hb2, label='Heat Stress / SEVI Score')
plt.title('Ahmedabad City: Socio-Economic Heat Stress Map', fontsize=16)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.tight_layout()
plt.savefig(os.path.join(out_dir, "Ahmedabad_Heat_Stress_Map.png"), dpi=300, bbox_inches='tight')
plt.close()

print("Optimized Hexbin Maps successfully generated in 'deliverables' directory.")
