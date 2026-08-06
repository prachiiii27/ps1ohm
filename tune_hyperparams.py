import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

def main():
    print("Loading data...")
    df = pd.read_csv('model_training_data.csv')

    features = [
        'Albedo_Liang_S2', 'NDVI_Greenness', 'NDMI_Moisture', 'BSI_Bare_Soil', 
        'FVC_Veg_Cover', 'Thermal_Admittance_cG', 'NDVI_Neighborhood_Mean', 
        'Albedo_Neighborhood_Mean', 'Exponential_Decay_Water', 
        'Exponential_Decay_Veg', 'Population_Density_GHSL', 'GHSL_Built_Surface',
        'PM25_Air_Pollution', 'PM10_Air_Pollution', 'NO2_Air_Pollution',
        'X_Coord', 'Y_Coord'
    ]
    target = 'LST_Celsius'

    X = df[features].values
    y = df[target].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    param_distributions = {
        'n_estimators': [1000, 1500, 2000, 2500],
        'learning_rate': [0.01, 0.015, 0.02, 0.025, 0.03],
        'max_depth': [10, 12, 14, 16],
        'subsample': [0.75, 0.8, 0.85, 0.9],
        'colsample_bytree': [0.75, 0.8, 0.85, 0.9],
        'min_child_weight': [1, 2, 3, 4],
        'gamma': [0.0, 0.05, 0.1, 0.15]
    }

    print("Starting Randomized Search (50 iterations)...")
    xgb_model = xgb.XGBRegressor(objective='reg:squarederror', random_state=42, n_jobs=-1)

    random_search = RandomizedSearchCV(
        estimator=xgb_model,
        param_distributions=param_distributions,
        n_iter=50,
        scoring='r2',
        cv=3,
        verbose=1,
        random_state=42,
        n_jobs=-1
    )

    random_search.fit(X_train, y_train)

    print(f"\nBest Parameters: {random_search.best_params_}")
    best_model = random_search.best_estimator_

    y_pred = best_model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    print(f"\nBest Test R2: {r2:.4f}")
    print(f"Best Test MAE: {mae:.4f}")

if __name__ == '__main__':
    main()
