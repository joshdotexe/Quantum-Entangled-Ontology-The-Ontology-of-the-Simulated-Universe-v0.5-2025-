@echo off
REM OSIU v0.8 Runner (Windows, with plotting)
SETLOCAL
cd /d %~dp0

IF NOT EXIST src\__init__.py type NUL > src\__init__.py
IF NOT EXIST src\model\__init__.py type NUL > src\model\__init__.py
IF NOT EXIST src\etl\__init__.py type NUL > src\etl\__init__.py
IF NOT EXIST src\viz\__init__.py type NUL > src\viz\__init__.py

IF NOT EXIST .venv (
  python -m venv .venv
)
CALL .venv\Scripts\activate
python -m pip install --upgrade pip wheel setuptools
pip install -r requirements.txt

echo === Normalize indicators ===
python -m src.model.fit_latents --config configs\indicators.yaml --normalize-only

echo === Fit sigma weights (KL) ===
python -m src.model.fit_weights --config configs\indicators.yaml

echo === Build latents and compute M ===
python -m src.model.fit_latents --config configs\indicators.yaml
python -m src.model.compute_M --config configs\indicators.yaml


echo === Generate plots ===
python -c "from src.viz.plots import plot_timeseries, plot_M_heatmap; print(plot_timeseries('data/processed/latents.csv')); print(plot_M_heatmap('data/processed/M_timeseries.csv'))"

echo === Done v0.8 pipeline ===
ENDLOCAL
