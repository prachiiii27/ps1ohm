import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import xgboost as xgb
import shap

# Create directory
out_dir = "shap_analysis"
os.makedirs(out_dir, exist_ok=True)

print("Loading data...")
df = pd.read_csv("model_training_data.csv")

# Ensure all columns are numeric
df = df.select_dtypes(include=[np.number])

# Drop constant pollution columns as per the 14-feature specification
pollution_cols = ['PM25_Air_Pollution', 'PM10_Air_Pollution', 'NO2_Air_Pollution']
df = df.drop(columns=[col for col in pollution_cols if col in df.columns])

# Define features and target
target_col = 'LST_Celsius'
if target_col not in df.columns:
    target_col = df.columns[0]

y = df[target_col]
X = df.drop(columns=[target_col])

print("1. Generating Pearson Correlation Matrix...")
plt.figure(figsize=(12, 10))
corr = df.corr(method='pearson')
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1)
plt.title("Pearson Correlation Matrix")
plt.tight_layout()
plt.savefig(os.path.join(out_dir, "pearson_correlation.png"), dpi=300)
plt.close()

print("2. Training XGBoost Model for SHAP Analysis...")
model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=6, random_state=42)
model.fit(X, y)

print("3. Calculating SHAP Values...")
# Use a sample if the dataset is too large to save time
if len(X) > 10000:
    X_sample = X.sample(10000, random_state=42)
else:
    X_sample = X

explainer = shap.TreeExplainer(model)
shap_values = explainer(X_sample)

print("4. Generating SHAP Summary Plot (Beeswarm)...")
plt.figure(figsize=(10, 8))
shap.summary_plot(shap_values, X_sample, show=False)
plt.title("SHAP Summary Plot (Impact on LST)")
plt.tight_layout()
plt.savefig(os.path.join(out_dir, "shap_summary_beeswarm.png"), dpi=300)
plt.close()

print("5. Generating SHAP Feature Importance (Bar)...")
plt.figure(figsize=(10, 8))
shap.summary_plot(shap_values, X_sample, plot_type="bar", show=False)
plt.title("SHAP Feature Importance (Mean Absolute Impact)")
plt.tight_layout()
plt.savefig(os.path.join(out_dir, "shap_feature_importance.png"), dpi=300)
plt.close()

print("6. Generating Separate Sensitivity Analysis Plots for the 3 Cooling Levers...")
# Explicitly target the 3 actionable cooling levers
cooling_levers = ['Albedo_Liang_S2', 'NDVI_Greenness', 'NDMI_Moisture']

for feature in cooling_levers:
    if feature in X.columns:
        plt.figure(figsize=(8, 6))
        # Plot the SHAP dependence for this specific feature
        shap.dependence_plot(feature, shap_values.values, X_sample, show=False)
        
        # Make the title beautiful for the presentation
        clean_name = feature.replace('_', ' ').replace('Liang S2', '').strip()
        plt.title(f"Sensitivity Analysis: {clean_name}\n(Impact on LST)", fontsize=14, pad=20)
        plt.tight_layout()
        
        plt.savefig(os.path.join(out_dir, f"Sensitivity_Analysis_{feature}.png"), dpi=300, bbox_inches='tight')
        plt.close()

print("All individual sensitivity analyses successfully saved!")
