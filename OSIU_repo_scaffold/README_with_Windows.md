# Ontology of the Simulated Universe — Repo Scaffold (v0.6-ready)

Minimal, working code scaffold to fetch indicators, normalize to latent variables (κ, σ, ρ, φ),
and compute the moral–informational gradient **𝓜(t) = [κ/(σ+ε)] · ρ · φ**.

> This README includes **both** Linux/macOS and Windows instructions.

---

## Quickstart (Linux/macOS)

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

---

## Quickstart (Windows / PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# Fetch data (World Bank API + OWID stub)
python src\etl\fetch_all.py --config configs\datasources.yaml

# Validate schema
python src\etl\validate_schema.py --schema data\metadata\indicators_schema.csv --glob "data/raw/*.csv"

# Normalize and compute latents
python src\model\fit_latents.py --config configs\indicators.yaml

# Compute the moral gradient M(t)
python src\model\compute_M.py --config configs\indicators.yaml

# Generate plots
python -c "from src.viz.plots import plot_timeseries, plot_M_heatmap; print(plot_timeseries('data/processed/latents.csv')); print(plot_M_heatmap('data/processed/M_timeseries.csv'))"
```

Or just run the included batch file:

```powershell
.un_all.bat
```

This will create a virtual environment, install dependencies, and run the entire pipeline automatically.

---

## Manual Data (all OS)

Place the following CSVs into `data/raw/`:

- `ucdp_conflict.csv`
- `happiness_index.csv`
- `diversity_index.csv`

Each must have columns: `region,year,value,id`.

Example rows:
```csv
region,year,value,id
USA,2020,0.4,ucdp_conflict
USA,2021,0.3,ucdp_conflict
```

---

## Outputs

- Normalized indicators → `data/interim/indicators_normalized.csv`
- Latent variables → `data/processed/latents.csv`  (kappa, sigma, rho, phi)
- Moral gradient → `data/processed/M_timeseries.csv`
- Plots → `results/figures/`

---

## Notes

- The Windows batch script is provided as `run_all.bat` in repo root.
- GNU Make is optional (used for Linux/macOS convenience). The same steps are executed by the batch file on Windows.
