
import argparse
import pandas as pd
from pathlib import Path

def main(url: str, outdir: str = "data/raw"):
    out = Path(outdir); out.mkdir(parents=True, exist_ok=True)
    # We do not fetch in this offline scaffold; we just record placeholder instructions.
    meta = pd.DataFrame([{"note": "Download OWID energy CSV from the configured URL and place under data/raw/owid_energy.csv"}])
    meta.to_csv(out / "OWID_README.csv", index=False)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=False, default="https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv")
    ap.add_argument("--outdir", default="data/raw")
    args = ap.parse_args()
    main(args.url, args.outdir)
