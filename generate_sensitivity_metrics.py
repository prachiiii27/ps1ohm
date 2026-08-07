import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xgboost as xgb
import shap
from scipy.stats import linregress

out_dir = "shap_analysis"
os.makedirs(out_dir, exist_ok=True)

print("Loading data...")
df = pd.read_csv("model_training_data.csv")
df = df.select_dtypes(include=[np.number])

pollution_cols = ['PM25_Air_Pollution', 'PM10_Air_Pollution', 'NO2_Air_Pollution']
df = df.drop(columns=[col for col in pollution_cols if col in df.columns])

target_col = 'LST_Celsius'
if target_col not in df.columns:
    target_col = df.columns[0]

y = df[target_col]
X = df.drop(columns=[target_col])

print("Training model...")
model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=6, random_state=42)
model.fit(X, y)

print("Calculating SHAP...")
explainer = shap.TreeExplainer(model)
shap_values = explainer(X)
shap_vals = shap_values.values

# Get top 4 features that *reduce* heat (so we look for negative correlation with LST)
# Actually let's just pick the actionable cooling levers: Albedo, Vegetation, Moisture
cooling_levers = ['Albedo_Liang_S2', 'NDVI_Greenness', 'NDMI_Moisture', 'FVC_Veg_Cover']
# Ensure they exist
cooling_levers = [f for f in cooling_levers if f in X.columns]

results = {}
for feature in cooling_levers:
    idx = X.columns.get_loc(feature)
    feat_data = X[feature].values
    shap_data = shap_vals[:, idx]
    
    # Calculate slope: how much SHAP (LST) changes per 1 unit of feature
    slope, intercept, r_value, p_value, std_err = linregress(feat_data, shap_data)
    
    # For a standard actionable change (e.g., +0.1 increase in index)
    # 0.1 is a 10% increase in Albedo/NDVI/FVC which is realistic
    temp_drop = slope * 0.1 
    
    # We want absolute temperature drop (so if slope is -10, temp_drop is -1.0, which means 1.0 degree reduction)
    results[feature] = abs(temp_drop) if temp_drop < 0 else -abs(temp_drop) # negative if it somehow heats

# Plot the actionable sensitivity
features_clean = [f.replace('_', ' ') for f in results.keys()]
drops = list(results.values())

plt.figure(figsize=(10, 6))
bars = plt.barh(features_clean, drops, color='dodgerblue')
plt.axvline(0, color='black', linewidth=1)
plt.xlabel('Expected LST Reduction (°C) per 10% (+0.1) Increase in Feature', fontsize=12)
plt.title('Actionable Sensitivity: Temperature Drop via Cooling Levers', fontsize=14)

# Add exact numbers to bars
for bar in bars:
    width = bar.get_width()
    plt.text(width + 0.02, bar.get_y() + bar.get_height()/2, f"-{width:.2f} °C", 
             va='center', ha='left', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(out_dir, "actionable_sensitivity_temp_drop.png"), dpi=300)
plt.close()

print("\n--- ACTIONABLE SENSITIVITY RESULTS ---")
for f, d in results.items():
    print(f"A +0.1 (10%) increase in {f} results in a {d:.2f} °C drop in Land Surface Temperature.")
