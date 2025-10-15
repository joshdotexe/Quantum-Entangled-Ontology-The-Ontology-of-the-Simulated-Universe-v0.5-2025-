
import argparse
from pathlib import Path
import pandas as pd
import yaml

def main(config_path: str):
    cfg = yaml.safe_load(Path(config_path).read_text())
    eps = float(cfg["output"].get("epsilon", 0.05))
    latents_fp = Path(cfg["output"]["processed_dir"]) / "latents.csv"
    df = pd.read_csv(latents_fp)
    for col in ["kappa","sigma","rho","phi"]:
        if col not in df.columns:
            raise SystemExit(f"Missing latent column: {col}")
    df["M"] = (df["kappa"] / (df["sigma"] + eps)) * df["rho"] * df["phi"]
    out_fp = Path(cfg["output"]["processed_dir"]) / "M_timeseries.csv"
    df[["region","year","M"]].to_csv(out_fp, index=False)
    print("Wrote", out_fp)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    main(args.config)
