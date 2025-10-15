@echo off
REM OSIU Pipeline Runner (Windows)
SETLOCAL
cd /d %~dp0

REM Ensure package structure
IF NOT EXIST src\__init__.py type NUL > src\__init__.py
IF NOT EXIST src\etl\__init__.py type NUL > src\etl\__init__.py
IF NOT EXIST src\model\__init__.py type NUL > src\model\__init__.py
IF NOT EXIST src\viz\__init__.py type NUL > src\viz\__init__.py

REM Create venv if needed
IF NOT EXIST .venv (
  python -m venv .venv
)

CALL .venv\Scripts\activate

REM Install deps
python -m pip install --upgrade pip wheel setuptools
pip install -r requirements.txt

echo.
echo === Fetch data ===
python -m src.etl.fetch_all --config configs\datasources.yaml

echo.
echo === Validate schema ===
python -m src.etl.validate_schema --schema data\metadata\indicators_schema.csv --glob "data/raw/*.csv"

echo.
echo === Normalize indicators and compute latents ===
python -m src.model.fit_latents --config configs\indicators.yaml

echo.
echo === Compute moral gradient M(t) ===
python -m src.model.compute_M --config configs\indicators.yaml

echo.
echo === Generate plots ===
python -c "from src.viz.plots import plot_timeseries, plot_M_heatmap; print(plot_timeseries('data/processed/latents.csv')); print(plot_M_heatmap('data/processed/M_timeseries.csv'))"

echo.
echo Done. Check 'data\interim', 'data\processed', and 'results\figures'.
ENDLOCAL