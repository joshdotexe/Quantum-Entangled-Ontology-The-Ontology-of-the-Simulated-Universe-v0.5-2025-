
# Ontology of the Simulated Universe — Repo Scaffold (v0.6-ready)

Minimal, working code scaffold to fetch indicators, normalize to latent variables (κ, σ, ρ, φ),
and compute the moral–informational gradient **𝓜(t) = [κ/(σ+ε)] · ρ · φ**.


## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Edit configs/datasources.yaml and configs/indicators.yaml as needed

make fetch        # pulls World Bank (and stubs OWID)
make validate     # checks raw CSV schema
make normalize    # builds data/interim/indicators_normalized.csv
make fit_latents  # builds data/processed/latents.csv
make compute_M    # builds data/processed/M_timeseries.csv
make plots        # writes results/figures/*
make all          # runs the whole pipeline
```
