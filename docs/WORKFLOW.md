# Development Workflow

This document describes how to work on the Air Quality Sensor Calibration project in a reproducible and reviewable way.

The project is intended to demonstrate scientific data analysis, Python software engineering, and baseline machine learning on noisy air-quality sensor data. The workflow below is written to make development decisions explicit rather than hidden in the dashboard.

## 1. Environment Setup

Create a virtual environment from the repository root:

```powershell
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell activation is blocked, commands can be run directly through the environment interpreter:

```powershell
.\venv\Scripts\python.exe -m pytest tests -p no:cacheprovider
.\venv\Scripts\python.exe -m streamlit run app.py
```

## 2. Running the Dashboard

Start the Streamlit app:

```powershell
streamlit run app.py
```

or:

```powershell
.\venv\Scripts\python.exe -m streamlit run app.py
```

Open:

```text
http://localhost:8501
```

## 3. Running Tests

Run the test suite before committing:

```powershell
pytest tests -p no:cacheprovider
```

The `-p no:cacheprovider` flag avoids Windows permission issues with pytest cache files in some restricted environments.

## 4. Data Handling Rules

The original dataset has several format-specific constraints:

- The CSV uses `;` as the separator.
- Decimal values use commas.
- Missing values are encoded as `-200`.
- `Date` and `Time` must be parsed into a timestamp.
- Empty trailing columns and rows can appear because of the original CSV layout.

The canonical loading logic is in `src/utils/data_loader.py`. Other modules should call `load_air_quality_data()` instead of reimplementing CSV parsing.

## 5. Missing-Value Policy

Missing values are handled in two stages:

- During loading, all `-200` sentinel values are converted to `NaN`.
- During modelling, missing feature values are imputed with `SimpleImputer(strategy="median")`.

Rows with missing target values are excluded from modelling. Feature rows are not globally dropped because doing so would discard useful observations.

## 6. Feature Engineering Rules

Feature engineering is centralized in `src/utils/preprocessing.py`.

Current modelling features include:

- metal oxide sensor responses
- temperature
- relative humidity
- absolute humidity
- cyclic hour features
- cyclic month features
- day-of-week feature

Reference analyzer columns other than the selected target are intentionally excluded from the model feature matrix. This reduces target leakage and keeps the task closer to sensor calibration.

## 7. Model Evaluation Rules

The modelling task is regression, not classification.

Evaluation uses:

- chronological holdout split
- time-series cross-validation on the training period
- MAE
- RMSE
- R2
- dummy median baseline

Random splitting should not be used as the only evaluation strategy because the dataset is time ordered and may contain sensor drift or concept drift.

## 8. Correlation and Network Analysis

The sensor analysis page supports:

- Pearson correlation for linear relationships
- Spearman correlation for monotonic rank-based relationships
- p-value matrices
- adjacency matrices
- filtered correlation network graphs

An edge is kept when:

```text
abs(correlation) >= threshold
p-value <= alpha
```

P-values should not be interpreted alone. With thousands of hourly observations, small p-values can appear even for relationships that are not practically strong.

## 9. Adding a New Model

To add a new regression model:

1. Add it to `make_regression_models()` in `src/models/regression.py`.
2. Keep preprocessing inside a scikit-learn `Pipeline`.
3. Add scaling only when the model family needs it.
4. Verify that the model supports missing-value handling through the pipeline.
5. Run the test suite.
6. Update the modelling explanation in the dashboard and docs if the model changes the interpretation.

## 10. Adding a New Dashboard Page

New Streamlit pages should follow these rules:

- Keep computation-heavy or reusable logic in `src/`.
- Keep page files focused on UI and interpretation.
- Add an expander explaining how to read each non-trivial graph.
- Avoid making scientific claims that are stronger than the analysis supports.
- Add tests for any new non-UI logic.

## 11. Documentation Workflow

Documentation exists at two levels:

- Markdown documents in `docs/` for humans reading the repository.
- Sphinx documentation in `docs/source/` for structured API and workflow documentation.

Build Sphinx docs with:

```powershell
sphinx-build -b html docs/source docs/build/html
```

Generated HTML files are not committed.

## 12. Pre-Commit Checklist

Before committing:

- Run `pytest tests -p no:cacheprovider`.
- Check that Streamlit starts.
- Check that new text does not overstate scientific claims.
- Confirm that missing-value handling still treats `-200` as invalid.
- Confirm that model features do not include leakage-prone `GT` columns.
- Update README or docs if commands, models, or workflow assumptions change.

## 13. Known Limitations

The project is a reproducible baseline, not a production monitoring system.

Current limitations:

- no explicit drift-correction algorithm
- no prediction intervals or uncertainty estimates
- no real-time sensor ingestion
- no database storage
- no operational model monitoring
- no regulatory air-quality certification
