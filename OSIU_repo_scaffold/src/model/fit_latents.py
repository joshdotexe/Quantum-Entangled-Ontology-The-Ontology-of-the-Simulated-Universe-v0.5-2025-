
import argparse, json
import pandas as pd
import numpy as np
from pathlib import Path
import yaml

def minmax(series: pd.Series):
    s = series.astype(float)
    mn, mx = np.nanmin(s), np.nanmax(s)
    if mx - mn == 0:
        return pd.Series(np.zeros(len(s)), index=s.index)
    return (s - mn) / (mx - mn)

def normalize_indicators(raw_dir: str, cfg: dict) -> pd.DataFrame:
    # Concatenate all raw files
    raw_files = list(Path(raw_dir).glob("*.csv"))
    frames = []
    for fp in raw_files:
        try:
            df = pd.read_csv(fp)
            frames.append(df)
        except Exception:
            continue
    if not frames:
        raise SystemExit("No raw data found.")
    df = pd.concat(frames, ignore_index=True)
    # Keep required columns
    df = df[["region","year","value","id"]].dropna()
    # Normalize per id
    df["norm"] = df.groupby("id")["value"].transform(minmax)
    return df

def build_latents(df_norm: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    out_rows = []
    for latent, spec in cfg["latents"].items():
        for ind in spec["indicators"]:
            id_ = ind["id"]
            w = float(ind.get("weight", 1.0))
            subset = df_norm[df_norm["id"] == id_][["region","year","norm"]].copy()
            subset.rename(columns={"norm": f"{latent}_part"}, inplace=True)
            subset["weight"] = w
            subset["id"] = id_
            out_rows.append(subset)
    parts = pd.concat(out_rows, ignore_index=True)
    # compute per-latent weighted average
    latents = []
    for latent in cfg["latents"].keys():
        sub = parts[parts["id"].isin([i["id"] for i in cfg["latents"][latent]["indicators"]])].copy()
        # compute weighted average explicitly to avoid groupby.apply index quirks
        sub["_wv"] = sub[f"{latent}_part"] * sub["weight"]
        tmp = (
            sub.groupby(["region", "year"], as_index=False)
            .agg({"_wv": "sum", "weight": "sum"})
        )
        tmp[latent] = tmp["_wv"] / tmp["weight"].replace(0, np.nan)
        tmp = tmp[["region", "year", latent]]
        latents.append(tmp)
    L = latents[0]
    for nxt in latents[1:]:
        L = L.merge(nxt, on=["region","year"], how="outer")
    return L.sort_values(["region","year"]).reset_index(drop=True)

def main(config_path: str, normalize_only: bool=False):
    cfg = yaml.safe_load(Path(config_path).read_text())
    interim = Path(cfg["output"]["interim_dir"]); interim.mkdir(parents=True, exist_ok=True)
    processed = Path(cfg["output"]["processed_dir"]); processed.mkdir(parents=True, exist_ok=True)

    df_norm = normalize_indicators("data/raw", cfg)
    df_norm.to_csv(interim / "indicators_normalized.csv", index=False)
    if normalize_only:
        print("Wrote", interim / "indicators_normalized.csv")
        return
    latents = build_latents(df_norm, cfg)
    latents.to_csv(processed / "latents.csv", index=False)
    print("Wrote", processed / "latents.csv")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--normalize-only", action="store_true")
    args = ap.parse_args()
    main(args.config, normalize_only=args.normalize_only)
