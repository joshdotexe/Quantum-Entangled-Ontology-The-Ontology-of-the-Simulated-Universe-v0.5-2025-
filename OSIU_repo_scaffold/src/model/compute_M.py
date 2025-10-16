import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import yaml

EPS = 1e-6

def _impute_groupwise(df, cols):
    """
    Safe per-region time imputation:
    1) Sort by (region, year) and reset row index
    2) groupby('region').transform(interpolate) -> preserves row alignment
    3) per-region mean fill, then global median fallback
    4) restore original row order
    """
    # Preserve original row order
    df = df.copy()
    df["_row"] = np.arange(len(df))

    # Coerce year to integer (e.g., 2000.0 -> 2000)
    # If you prefer years as floats, comment these two lines.
    if "year" in df.columns:
        df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")

    # Work in sorted space, then restore
    work = df.sort_values(["region", "year"]).reset_index(drop=True)

    # Interpolate within each region, then fill means/median
    for c in cols:
        if c not in work.columns:
            work[c] = np.nan

        # time-direction interpolation per region
        work[c] = work.groupby("region")[c].transform(
            lambda s: s.interpolate(limit_direction="both")
        )

        # per-region mean fill
        region_means = work.groupby("region")[c].transform(lambda s: s.mean(skipna=True))
        work[c] = work[c].fillna(region_means)

        # global median fallback
        work[c] = work[c].fillna(work[c].median(skipna=True))

    # Restore original row order
    work = work.sort_values("_row").drop(columns=["_row"])
    return work

def _clip01(df, cols):
    for c in cols:
        df[c] = df[c].clip(0.0, 1.0)
    return df

def main(config_path: str):
    cfg = yaml.safe_load(Path(config_path).read_text())
    processed = Path(cfg["output"]["processed_dir"])
    processed.mkdir(parents=True, exist_ok=True)

    latents_fp = processed / "latents.csv"
    if not latents_fp.exists():
        raise SystemExit(f"Missing {latents_fp}. Run fit_latents first.")

    df = pd.read_csv(latents_fp)

    # Ensure columns exist
    for c in ["region","year","kappa","sigma","rho","phi"]:
        if c not in df.columns:
            df[c] = np.nan

    # Keep a copy of original (to check how much signal we had before imputation)
    df_orig = df.copy()

    # Impute & clamp to [0,1]
    df = _impute_groupwise(df, ["kappa","sigma","rho","phi"])
    df = _clip01(df, ["kappa","sigma","rho","phi"])

    # Fallback priors if a latent is globally missing (avoids all-NaN M)
    # priors = {"sigma": 0.5, "phi": 0.5}  # neutral, configurable later
    # for c, prior in priors.items():
    #     if df[c].isna().all():
    #         print(f"[warn] '{c}' has no data globally; filling with prior={prior}.")
    #         df[c] = prior


    # Require at least two non-NaN latents originally to trust the row
    signal_count = df_orig[["kappa","sigma","rho","phi"]].notna().sum(axis=1)
    df = df.loc[signal_count.values >= 2].copy()

    # Compute M with epsilon guard
    df["M_raw"] = (df["kappa"] / (df["sigma"] + EPS)) * df["rho"] * df["phi"]
    # Clip for visualization sanity (raw kept for analysis)
    df["M"] = df["M_raw"].clip(lower=-0.1, upper=0.1)

    # Coverage diagnostics
    cov = (
        df_orig.groupby("region")[["kappa","sigma","rho","phi"]]
               .apply(lambda g: g.notna().mean())
               .reset_index()
               .rename(columns={"kappa":"cov_kappa","sigma":"cov_sigma",
                                "rho":"cov_rho","phi":"cov_phi"})
    )

    df.to_csv(processed / "M_timeseries.csv", index=False)
    cov.to_csv(processed / "coverage_latents_by_region.csv", index=False)
    print("Wrote", processed / "M_timeseries.csv")
    print("Coverage by region ->", processed / "coverage_latents_by_region.csv")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    main(args.config)
