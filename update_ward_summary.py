import json
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, shape
import os

print("Loading data...")
# Load Wards GeoJSON
with open('data/wards_real.geojson') as f:
    geo_data = json.load(f)

# Load 100m Parquet
df_grid = pd.read_parquet('data/ahmedabad_grid_100m.parquet')

print("Creating GeoDataFrame...")
geometry = [Point(xy) for xy in zip(df_grid['lon'], df_grid['lat'])]
gdf_points = gpd.GeoDataFrame(df_grid, geometry=geometry, crs="EPSG:4326")

ward_summaries = []
for feature in geo_data['features']:
    ward_id = feature['properties']['ward_id']
    geom = shape(feature['geometry'])
    
    # Filter points inside ward
    minx, miny, maxx, maxy = geom.bounds
    gdf_sub = gdf_points.cx[minx:maxx, miny:maxy]
    mask = gdf_sub.geometry.apply(lambda g: geom.contains(g))
    pts_in_ward = gdf_sub[mask]
    
    if not pts_in_ward.empty:
        built_pct = (pts_in_ward['built_fraction'].mean() * 100)
        veg_pct = (pts_in_ward['green_ratio'].mean() * 100)
        # Approximate Water (LULC=1 is water in some datasets, wait, app.py says: x==1 is water, x==3 is barren)
        water_pct = (pts_in_ward['lulc_class'] == 1).mean() * 100
        barren_pct = (pts_in_ward['lulc_class'] == 3).mean() * 100
        
        # Normalize to 100
        total = built_pct + veg_pct + water_pct + barren_pct
        if total > 0:
            built_pct = (built_pct / total) * 100
            veg_pct = (veg_pct / total) * 100
            water_pct = (water_pct / total) * 100
            barren_pct = (barren_pct / total) * 100
    else:
        built_pct, veg_pct, water_pct, barren_pct = 50.0, 10.0, 0.0, 40.0
        
    ward_summaries.append({
        'ward_id': ward_id,
        'built_pct': built_pct,
        'veg_pct': veg_pct,
        'water_pct': water_pct,
        'barren_pct': barren_pct
    })

df_ward_caps = pd.DataFrame(ward_summaries)

print("Updating sevi_ward_summary.json...")
df_sevi = pd.read_json('data/sevi_ward_summary.json')

# Merge
if 'built_pct' in df_sevi.columns:
    df_sevi = df_sevi.drop(columns=['built_pct', 'veg_pct', 'water_pct', 'barren_pct'])
    
df_sevi = pd.merge(df_sevi, df_ward_caps, on='ward_id', how='left')

# Fill NaNs
df_sevi['built_pct'] = df_sevi['built_pct'].fillna(50.0)
df_sevi['veg_pct'] = df_sevi['veg_pct'].fillna(10.0)
df_sevi['water_pct'] = df_sevi['water_pct'].fillna(0.0)
df_sevi['barren_pct'] = df_sevi['barren_pct'].fillna(40.0)

df_sevi.to_json('data/sevi_ward_summary.json', orient='records')
print("Successfully updated sevi_ward_summary.json with Feasibility Caps!")
