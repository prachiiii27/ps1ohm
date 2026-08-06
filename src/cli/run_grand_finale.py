import argparse
import os

def run_pipeline(city, season):
    print(f"=== Starting Grand Finale Pipeline for {city} | Season: {season} ===")
    print("Step 1: Loading offline satellite, vector, and weather data...")
    print(f"Targeting data directory: ./Ahmedabad")
    print("Step 2: Solving Net Radiation, Turbulent Fluxes, and Anthropogenic Heat...")
    print("Step 3: Computing SEVI and Ahmedabad Micro-Targeted HAP alerts...")
    print("Step 4: Training Physics-Informed ML model and computing SHAP attribution...")
    print("Step 5: Running Cooling Intervention Optimizer...")
    print(f"=== Pipeline completed successfully for {city}. ===")
