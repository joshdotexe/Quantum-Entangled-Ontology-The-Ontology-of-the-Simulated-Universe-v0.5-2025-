
import argparse, sys
from pathlib import Path
from src.etl.fetch_worldbank import main as wb_main
from src.etl.fetch_owid import main as owid_main

def main(config_path: str):
    wb_main(config_path, outdir="data/raw")
    owid_main(url=None, outdir="data/raw")
    # Emit instructions for manual files
    expected = ["ucdp_conflict.csv", "happiness_index.csv", "diversity_index.csv"]
    missing = [f for f in expected if not Path("data/raw", f).exists()]
    if missing:
        print("NOTE: Place these manual datasets into data/raw/:", ", ".join(missing))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    main(args.config)
