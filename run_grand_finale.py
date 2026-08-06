import sys
from src.cli.run_grand_finale import run_pipeline

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Grand Finale Urban Heat Pipeline")
    parser.add_argument('--city', type=str, required=True, help="Target City (e.g. Ahmedabad)")
    parser.add_argument('--season', type=str, default='all', help="Season to run (e.g. May_2024)")
    args = parser.parse_args()
    
    run_pipeline(args.city, args.season)
