import os
import sys
import numpy as np
import rasterio
import pandas as pd
import xarray as xr
import geopandas as gpd
from rasterio.features import rasterize
from rasterio.warp import reproject, Resampling
from scipy.ndimage import gaussian_filter, distance_transform_edt

sys.path.append(r"c:\Users\tanya\OneDrive\Desktop\ps1ohm")
from src.physics.net_radiation import calculate_liang_albedo, calculate_net_radiation, calculate_atmospheric_emissivity
from src.physics.turbulent_fluxes import calculate_sensible_heat_flux, calculate_aerodynamic_resistance
from src.physics.ground_flux import calculate_ground_heat_flux
from src.physics.seb_residual_qf import calculate_total_anthropogenic_heat
from src.modeling.dataset_builder import build_feature_matrix
from src.modeling.physics_informed_ml import PhysicsInformedHeatModel
from src.modeling.driver_attribution import calculate_shap_values

def prepare_data_for_ml():
    print("Step 1: Extracting UN-MOCKED features for ML training (Jan 2023)...")
    base_dir = r"c:\Users\tanya\OneDrive\Desktop\ps1ohm\Ahmedabad\Jan_2023"
    
    sentinel_path = os.path.join(base_dir, "remote_sensing", "sentinel2_Ahmedabad_Jan_2023.tif")
    landsat_path = os.path.join(base_dir, "remote_sensing", "landsat_Ahmedabad_Jan_2023.tif")
    lulc_path = os.path.join(base_dir, "remote_sensing", "lulc_dynamic_world_Ahmedabad_Jan_2023.tif")
    lulc_path = os.path.join(base_dir, "remote_sensing", "lulc_dynamic_world_Ahmedabad_Jan_2023.tif")
    gpkg_path = os.path.join(base_dir, "osm", "buildings_Ahmedabad.gpkg")
    streets_path = os.path.join(base_dir, "osm", "streets_Ahmedabad.gpkg")
    era5_dir = os.path.join(base_dir, "era5")
    ghsl_pop_path = r"c:\Users\tanya\OneDrive\Desktop\ps1ohm\GHSL\ghs_pop_e2025_r2023a_54009_100_v1_0_ind.tif"
    ghsl_built_path = r"c:\Users\tanya\OneDrive\Desktop\ps1ohm\GHSL\ghs_built_s_e2025_r2023a_54009_100_v1_0_ind.tif"

    with rasterio.open(sentinel_path) as src_s2:
        b2, b4, b8, b11, b12 = src_s2.read(1), src_s2.read(2), src_s2.read(3), src_s2.read(4), src_s2.read(5)
        profile = src_s2.profile
        transform = src_s2.transform
        albedo = calculate_liang_albedo(b2, b4, b8, b11, b12)

    with rasterio.open(landsat_path) as src_l8:
        t_s = src_l8.read(1)
        
    with rasterio.open(lulc_path) as src_lulc:
        lulc = src_lulc.read(1)
        
    min_rows, min_cols = min(albedo.shape[0], t_s.shape[0]), min(albedo.shape[1], t_s.shape[1])
    albedo, t_s, lulc = albedo[:min_rows, :min_cols], t_s[:min_rows, :min_cols], lulc[:min_rows, :min_cols]

    print(" -> Extracting true meteorology...")
    era5_file = [f for f in os.listdir(era5_dir) if f.endswith('.nc')][0]
    with xr.open_dataset(os.path.join(era5_dir, era5_file)) as ds:
        t2m_mean = ds['t2m'].mean().values.item()
        d2m_mean = ds['d2m'].mean().values.item()
        ssrd_mean = ds['ssrd'].mean().values.item()
        u10_mean = ds['u10'].mean().values.item()
        v10_mean = ds['v10'].mean().values.item()
        
    t_air = t2m_mean - 273.15
    t_air_k = t2m_mean
    sw_in = ssrd_mean / 3600.0
    wind_speed = np.sqrt(u10_mean**2 + v10_mean**2)
    e_a = 6.11 * (10 ** (7.5 * (d2m_mean - 273.15) / (237.3 + (d2m_mean - 273.15))))

    print(" -> Extracting Air Quality Pollution variables (PM2.5, PM10, NO2)...")
    aq_file = os.path.join(base_dir, "air_quality", "air_quality_openmeteo_Ahmedabad.csv")
    aq_df = pd.read_csv(aq_file)
    pm25_val = aq_df['PM25'].mean()
    pm10_val = aq_df['PM10'].mean()
    no2_val = aq_df['NO2'].mean()
    
    pm25_array = np.full_like(t_s, pm25_val, dtype=np.float32)
    pm10_array = np.full_like(t_s, pm10_val, dtype=np.float32)
    no2_array = np.full_like(t_s, no2_val, dtype=np.float32)

    print(" -> Rasterizing true building and street geometries...")
    try:
        gdf = gpd.read_file(gpkg_path, rows=5000)
        shapes = ((geom, 10.0) for geom in gdf.geometry)
        building_heights = rasterize(shapes, out_shape=(min_rows, min_cols), transform=transform, fill=0.0)
    except:
        building_heights = np.where(lulc == 1, 10.0, 0.0)
        
    try:
        gdf_streets = gpd.read_file(streets_path, rows=5000)
        street_shapes = ((geom, 1.0) for geom in gdf_streets.geometry)
        streets_raster = rasterize(street_shapes, out_shape=(min_rows, min_cols), transform=transform, fill=0.0)
        road_density = gaussian_filter(streets_raster.astype(float), sigma=10)
    except:
        road_density = np.zeros((min_rows, min_cols))
    
    # Physics Calculations
    t_s_k = t_s + 273.15
    lw_in = calculate_atmospheric_emissivity(e_a, t_air_k) * 5.67e-8 * (t_air_k**4)
    
    # INDEPENDENT Net Radiation
    r_n_indep = calculate_net_radiation(sw_in, lw_in, t_air_k, albedo)
    
    z_0 = np.where(building_heights > 0, building_heights * 0.1, 0.1)
    
    # Spectral Indices
    b2_m, b4_m, b8_m, b11_m = b2[:min_rows, :min_cols], b4[:min_rows, :min_cols], b8[:min_rows, :min_cols], b11[:min_rows, :min_cols]
    ndvi = (b8_m - b4_m) / (b8_m + b4_m + 1e-8)
    ndbi = (b11_m - b8_m) / (b11_m + b8_m + 1e-8)
    ndmi = (b8_m - b11_m) / (b8_m + b11_m + 1e-8)
    
    # Bare Soil Index (BSI)
    bsi = ((b11_m + b4_m) - (b8_m + b2_m)) / ((b11_m + b4_m) + (b8_m + b2_m) + 1e-8)
    
    # Fractional Vegetation Cover (FVC)
    ndvi_min, ndvi_max = np.percentile(ndvi, 5), np.percentile(ndvi, 95)
    fvc = np.clip((ndvi - ndvi_min) / (ndvi_max - ndvi_min + 1e-8), 0.0, 1.0)
    
    # Spatial Neighborhood (Heat Spillover via Gaussian Smoothing)
    ndvi_mean = gaussian_filter(ndvi, sigma=3)
    albedo_mean = gaussian_filter(albedo, sigma=3)
    
    # Plan Area Index (PAI) - smoothed footprint density
    footprint_mask = (building_heights > 0).astype(float)
    pai = gaussian_filter(footprint_mask, sigma=3)
    
    # --- PHASE 3 ADVANCED MATHEMATICAL FEATURES ---
    max_height = np.max(building_heights) + 1e-8
    true_svf = np.clip(1.0 - (building_heights / max_height), 0.2, 1.0)
    
    dist_water = np.exp(-distance_transform_edt(lulc != 3) / 100.0)
    dist_veg = np.exp(-distance_transform_edt(lulc != 2) / 100.0)
    
    c_g = np.select(
        [lulc == 1, lulc == 2, lulc == 3, lulc == 4], 
        [0.3, 0.15, 0.5, 0.2], 
        default=0.2
    )

    # --- PHASE 4: ANTHROPOGENIC FORCING (NO2 & POPULATION) ---
    print(" -> Extracting Anthropogenic Data (Population & GHSL Built)...")
        
    # GHSL Population & Built Surface Extraction (Dynamic Reprojection)
    pop_array = np.zeros_like(t_s, dtype=np.float32)
    ghsl_built_array = np.zeros_like(t_s, dtype=np.float32)
    try:
        with rasterio.open(ghsl_pop_path) as src_pop:
            reproject(
                source=rasterio.band(src_pop, 1),
                destination=pop_array,
                src_transform=src_pop.transform,
                src_crs=src_pop.crs,
                dst_transform=transform,
                dst_crs=profile['crs'],
                resampling=Resampling.average
            )
        with rasterio.open(ghsl_built_path) as src_built:
            reproject(
                source=rasterio.band(src_built, 1),
                destination=ghsl_built_array,
                src_transform=src_built.transform,
                src_crs=src_built.crs,
                dst_transform=transform,
                dst_crs=profile['crs'],
                resampling=Resampling.average
            )
    except Exception as e:
        print(f"   [Warning] GHSL Reprojection Failed: {e}. Falling back to LULC proxy.")
        pop_array = np.where(lulc == 1, 1000.0, 0.0)
        ghsl_built_array = np.where(lulc == 1, 1.0, 0.0)

    print("Step 2: Building Feature Matrix (Flattening spatial arrays)...")
    df = build_feature_matrix(
        t_s, albedo, r_n_indep, ndvi, ndbi, ndmi, ndvi_mean, albedo_mean, 
        true_svf, z_0, dist_water, dist_veg, c_g, bsi, fvc, pai, pop_array, road_density, ghsl_built_array,
        pm25_array, pm10_array, no2_array
    )
    
    # Generate Spatial Coordinates to help model learn urban clustering
    y_coords, x_coords = np.mgrid[0:min_rows, 0:min_cols]
    df['X_Coord'] = x_coords.flatten()
    df['Y_Coord'] = y_coords.flatten()
    
    df = df.dropna()
    df = df.sample(n=min(5000, len(df)), random_state=42)
    
    # Export for the Data Science Dashboard
    df.to_csv("model_training_data.csv", index=False)
    print(" -> Data successfully exported to model_training_data.csv for Dashboard.")
    
    return df

def run_ml_training():
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
    
    df = prepare_data_for_ml()
    
    y = df['LST_Celsius']
    X = df.drop(columns=['LST_Celsius'])
    
    # Train/Test Split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("\n--- ML Training Initialized ---")
    print(f"Training XGBoost on {len(X_train)} pixels, Testing on {len(X_test)} pixels with {len(X.columns)} physical features...")
    
    model = PhysicsInformedHeatModel()
    model.fit(X_train, y_train)
    
    print("\nModel successfully trained!")
    
    # Predict and evaluate
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    print("\n=== MACHINE LEARNING EVALUATION METRICS ===")
    print(f"R-Squared (R²): {r2:.4f} (Explains {r2*100:.1f}% of temperature variance)")
    print(f"Mean Absolute Error (MAE): {mae:.4f} °C")
    print(f"Root Mean Squared Error (RMSE): {rmse:.4f} °C")
    
    print("\nStep 3: Calculating SHAP Feature Importance (Driver Attribution)...")
    
    shap_values = calculate_shap_values(model, X_test)
    
    mean_shap = np.abs(shap_values).mean(axis=0)
    feature_importance = pd.DataFrame(list(zip(X.columns, mean_shap)), columns=['Feature', 'Importance'])
    feature_importance = feature_importance.sort_values(by='Importance', ascending=False)
    
    print("\n=== DRIVER ATTRIBUTION RESULTS ===")
    print("Which physical factors most strongly affect Urban Heat (LST)?")
    for idx, row in feature_importance.iterrows():
        print(f"{row['Feature']:25s} : {row['Importance']:.4f}")
        
    print("\nMachine Learning outputs ready.")

if __name__ == "__main__":
    run_ml_training()


