import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path
import textwrap

# === Utility ===
def _save_caption(path: str, text: str):
    """Save a plain-text caption file next to a figure."""
    caption_path = Path(path).with_suffix(".txt")
    caption_path.write_text(textwrap.fill(text, width=90), encoding="utf-8")

def _append_interpretation(fname: Path, var: str):
    """Append theoretical interpretation notes to each figure caption."""
    interpretations = {
        "kappa": (
            "\n\nInterpretation: If κ increases or remains stable across years, the system exhibits "
            "growing moral/institutional coherence. Declines suggest ethical fragmentation."
        ),
        "sigma": (
            "\n\nInterpretation: Lower σ corresponds to reduced systemic suffering (moral entropy). "
            "The theory predicts σ should gradually decline as κ and ρ stabilize."
        ),
        "rho": (
            "\n\nInterpretation: ρ should move in tandem with κ, reflecting resilient lawful regularity. "
            "Persistent divergence implies structural decoupling from coherence."
        ),
        "phi": (
            "\n\nInterpretation: φ rising with κ indicates healthy pluralism and adaptive diversity. "
            "Small oscillations are expected in adaptive systems; sharp drops imply rigidity."
        ),
        "M": (
            "\n\nInterpretation: A visible upward-bright trend/diagonal in M(t) across years and regions "
            "suggests theoretical support (convergence toward moral equilibrium). "
            "Noisy or flat gradients imply instability or incomplete latent alignment."
        ),
    }

    textfile = Path(fname).with_suffix(".txt")
    if textfile.exists():
        with open(textfile, "a", encoding="utf-8") as f:
            f.write(interpretations.get(var, ""))

def _write_theory_expectations():
    """Write a global interpretive guide for all figures."""
    outdir = Path("results/figures")
    outdir.mkdir(parents=True, exist_ok=True)
    msg = """Expected Empirical Patterns for Validation
------------------------------------------
1) κ (Kappa): should increase or stabilize over time; positive correlation with ρ and φ.
2) σ (Sigma): should gradually decline as κ and ρ improve (reduced moral entropy).
3) ρ (Rho): should track κ (coherence → regularity/resilience).
4) φ (Phi): should rise modestly with κ; mild oscillations are normal in adaptive pluralism.
5) M(t): should show a smooth, upward-bright trend across years/regions (ethical stabilization).

Quick Diagnostic Thresholds (heuristic)
---------------------------------------
• If σ rises while κ rises: mis-specified proxies or missing normalization.
• If M(t) is flat/noisy: latent coupling incomplete or inputs sparse.
• If φ collapses while κ, ρ stay high: ethical monoculture or reduced adaptability.
• Coverage check: require ≥2 observed latents pre-imputation per row for trustworthy M.

Notes
-----
These expectations follow the v0.8 FEP-constrained moral-informational model. They are descriptive
guides, not pass/fail tests; use them to triage data issues and refine proxy mappings.
"""
    (outdir / "theory_expectations.txt").write_text(msg, encoding="utf-8")

# === Latent Variable Time Series ===
def plot_timeseries(latents_csv: str):
    df = pd.read_csv(latents_csv)
    outdir = Path("results/figures")
    outdir.mkdir(parents=True, exist_ok=True)
    _write_theory_expectations()

    captions = {
        "kappa": (
            "Figure: κ (Kappa) – Governance/cooperative coherence. Higher values indicate stronger "
            "coordination, stability, and ethical alignment; an approximation to informational order."
        ),
        "sigma": (
            "Figure: σ (Sigma) – Systemic suffering load (moral entropy). Higher values indicate greater "
            "disorder/instability. Inverse of coherence."
        ),
        "rho": (
            "Figure: ρ (Rho) – Structural resilience and lawful regularity. Higher values indicate durable, "
            "consistent normative and institutional structure."
        ),
        "phi": (
            "Figure: φ (Phi) – Pluralism/adaptive diversity capacity. Higher values indicate moral "
            "responsiveness and inclusion across perspectives."
        ),
    }

    for var in ["kappa", "sigma", "rho", "phi"]:
        if var not in df.columns:
            continue

        plt.figure(figsize=(8, 4))
        for region, g in df.groupby("region"):
            plt.plot(g["year"], g[var], label=region, linewidth=1.8)
        plt.legend(loc="upper left", fontsize=8)
        plt.title(f"Temporal Evolution of {var.upper()}")
        plt.xlabel("Year")
        plt.ylabel("Normalized Value")

        # caption footer
        plt.figtext(
            0.5, -0.08, captions[var], wrap=True, ha="center", va="top",
            fontsize=8.5, style="italic",
        )

        plt.tight_layout()
        fname = outdir / f"latents_timeseries_{var}.png"
        plt.savefig(fname, dpi=300, bbox_inches="tight")
        plt.close()
        _save_caption(fname, captions[var])
        _append_interpretation(fname, var)

# === Moral Gradient Heatmap ===
def plot_M_heatmap(M_csv: str):
    df = pd.read_csv(M_csv)
    if df["M"].isna().all():
        print("All M values are NaN (nothing to plot). Check inputs.")
        return

    outdir = Path("results/figures")
    outdir.mkdir(parents=True, exist_ok=True)
    _write_theory_expectations()

    pivot = df.pivot(index="region", columns="year", values="M")
    plt.figure(figsize=(8, 4))
    im = plt.imshow(pivot, aspect="auto", cmap="magma", origin="lower")
    plt.colorbar(im, label="Moral Gradient M(t)")
    plt.xticks(range(len(pivot.columns)), pivot.columns, rotation=45)
    plt.yticks(range(len(pivot.index)), pivot.index)
    plt.title("Moral Gradient Heatmap (M(t))")

    caption_text = (
        "Figure: M(t) – Composite moral–informational gradient from {κ, σ, ρ, φ}. "
        "Lighter tones indicate higher ethical stability and informational coherence; "
        "darker tones indicate entropy/stress. Computed on normalized, weighted latents."
    )

    plt.figtext(
        0.5, -0.10, caption_text, wrap=True, ha="center", va="top",
        fontsize=8.5, style="italic",
    )

    plt.tight_layout()
    fname = outdir / "M_heatmap.png"
    plt.savefig(fname, dpi=300, bbox_inches="tight")
    plt.close()
    _save_caption(fname, caption_text)
    _append_interpretation(fname, "M")

    print(f"Wrote heatmap with caption to {fname}")
