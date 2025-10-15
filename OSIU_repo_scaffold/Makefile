
.PHONY: fetch validate normalize fit_latents fit_dynamics compute_M plots all

fetch:
	python -m src.etl.fetch_all --config configs/datasources.yaml

validate:
	python -m src.etl.validate_schema --schema data/metadata/indicators_schema.csv --glob 'data/raw/*.csv'

normalize:
	python -m src.model.fit_latents --normalize-only --config configs/indicators.yaml

fit_latents:
	python -m src.model.fit_latents --config configs/indicators.yaml

fit_dynamics:
	python -m src.model.fit_dynamics || echo 'fit_dynamics (optional) not implemented yet.'

compute_M:
	python -m src.model.compute_M --config configs/indicators.yaml

plots:
	python -c "from src.viz.plots import plot_timeseries, plot_M_heatmap; print(plot_timeseries('data/processed/latents.csv')); print(plot_M_heatmap('data/processed/M_timeseries.csv'))"

all: fetch validate normalize fit_latents compute_M plots
