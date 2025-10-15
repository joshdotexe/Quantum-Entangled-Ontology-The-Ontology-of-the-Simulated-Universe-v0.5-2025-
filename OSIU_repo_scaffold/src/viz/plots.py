
import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

FIG_DIR = Path("results/figures"); FIG_DIR.mkdir(parents=True, exist_ok=True)

def plot_timeseries(latents_csv: str):
    df = pd.read_csv(latents_csv)
    regions = sorted(df["region"].unique())
    for r in regions:
        sub = df[df["region"] == r].sort_values("year")
        plt.figure()
        for col in ["kappa","sigma","rho","phi"]:
            if col in sub.columns:
                plt.plot(sub["year"], sub[col], label=col)
        plt.xlabel("Year"); plt.ylabel("Index (0..1)"); plt.title(f"Latents — {r}")
        plt.legend()
        out = FIG_DIR / f"latents_{r}.png"
        plt.savefig(out, bbox_inches="tight", dpi=150)
        plt.close()
    return f"Wrote {len(regions)} time-series plots to {FIG_DIR}"

def plot_M_heatmap(M_csv: str):
    df = pd.read_csv(M_csv)
    piv = df.pivot(index="region", columns="year", values="M")
    plt.figure()
    plt.imshow(piv, aspect="auto")
    plt.colorbar(label="M")
    plt.yticks(range(len(piv.index)), piv.index)
    plt.xticks(range(len(piv.columns)), piv.columns, rotation=90)
    plt.title("Moral–Informational Gradient (M) — Heatmap")
    out = FIG_DIR / "M_heatmap.png"
    plt.savefig(out, bbox_inches="tight", dpi=180)
    plt.close()
    return f"Wrote heatmap to {out}"
