# Air Quality Sensor Calibration

Streamlit dashboard that calibrates low-cost gas sensors against a certified reference analyzer, using the public UCI Air Quality dataset.

**Live demo:** https://ml-air-quality-ayis.onrender.com/
(free hosting: the first load after a pause can take up to a minute)

## What it does

Low-cost metal-oxide sensors are cheap but noisy: they drift over time and react to more than one gas. This project treats calibration as a regression problem: sensor responses and weather variables are used to estimate the gas concentrations measured by a reference analyzer.

The dashboard has five pages:

| Page | Content |
| --- | --- |
| Data Overview | Dataset profile, variables by type, missing values per column, monthly data quality, numeric summary |
| Sensor Analysis | Temporal behaviour, sensor vs reference target, Pearson and Spearman correlations with p-values, correlation network filtered by strength and significance |
| Modeling | Regression benchmark on a selectable target, with chronological holdout and time-series cross-validation |
| Scientific Notes | Sensor drift, cross-sensitivity and modelling limits |
| Documentation | Technical documentation of the project |

## Methodology

- **Data cleaning:** the CSV uses `;` separators and decimal commas; missing values encoded as `-200` are converted to `NaN`; `Date` and `Time` are combined into a timestamp.
- **Features:** sensor responses (`PT08.S1`–`PT08.S5`), temperature, relative and absolute humidity, cyclic hour and month (sine/cosine) and day of week.
- **No leakage:** the other reference-analyzer measurements (`*(GT)` columns) are excluded from the features, so the model cannot use one certified measurement to predict another. A test enforces this.
- **Models:** scikit-learn pipelines with median imputation: a `DummyRegressor` baseline, Ridge, Random Forest and Gradient Boosting.
- **Evaluation:** chronological train/test split (earlier data for training, later data for testing) plus `TimeSeriesSplit` cross-validation, reported with MAE, RMSE and R².
- **Targets:** `CO(GT)`, `C6H6(GT)`, `NOx(GT)`, `NO2(GT)`.

## Tech stack

Python · pandas · NumPy · scikit-learn · SciPy · Streamlit · Plotly · pytest · Sphinx

## Project structure

```text
app.py                  Streamlit entry point (home page)
pages/                  Dashboard pages
src/
  config.py             Paths, column groups, targets, random seed
  data/                 UCI Air Quality dataset (CSV and XLSX)
  models/regression.py  Model suite and evaluation
  utils/
    data_loader.py      CSV parsing and cleaning
    preprocessing.py    Feature engineering and chronological split
    analysis.py         Profiles, correlations, p-values, correlation network
    metadata.py         Variable dictionary
  ui/theme.py           Dashboard styling
tests/                  pytest suite
docs/                   Architecture, workflow, notebooks, Sphinx sources
render.yaml             Render deployment
```

## Run locally

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m streamlit run app.py
```

Then open http://localhost:8501.

## Tests

```powershell
.\venv\Scripts\python.exe -m pytest tests -p no:cacheprovider
```

The suite covers data loading and sentinel handling, feature engineering, leakage exclusion, the chronological split, the regression benchmark, correlation p-values and the correlation network.

## Deployment

Deployed on Render as a Python web service (`render.yaml`):

```text
streamlit run app.py --server.headless true --server.port $PORT --server.address 0.0.0.0
```

## Documentation

- [docs/TECHNICAL_ARCHITECTURE.md](docs/TECHNICAL_ARCHITECTURE.md): architecture, data flow, modelling workflow and scientific limitations
- [docs/WORKFLOW.md](docs/WORKFLOW.md): development workflow and reproducibility rules
- [docs/air_quality_analysis_ml.ipynb](docs/air_quality_analysis_ml.ipynb): exploratory analysis and regression notebook
- Sphinx sources in `docs/source/`, built with `sphinx-build -b html docs/source docs/build/html`

## Limitations

- Sensor drift: the relationship between sensor signal and true concentration can change over time. Chronological evaluation takes this into account, but no explicit drift-correction algorithm is implemented.
- Cross-sensitivity: each sensor reacts to several gases, which limits how well one target can be isolated.
- The data comes from a single device over about one year; results do not transfer to other sites without recalibration.
- The models are baselines for comparison, not a tuned production calibration system.

## Data source

Air Quality dataset, UCI Machine Learning Repository: 9,357 hourly records (March 2004 to April 2005) from a gas multisensor device deployed in an Italian urban area, with reference concentrations from a certified analyzer.
