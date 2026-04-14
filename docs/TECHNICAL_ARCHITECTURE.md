# Technical Architecture

## Overview

This project is a modular Python and Streamlit application for analysing the UCI Air Quality dataset. The dataset contains hourly field measurements from an air-quality chemical multisensor device and certified reference analyzer measurements.

The project is designed as a portfolio-level scientific data analysis workflow. It is not a production monitoring platform.

## Architecture

```text
Streamlit UI
    |
    v
Analysis Pages
    |
    v
Reusable Python Modules
    |-- src/utils/data_loader.py
    |-- src/utils/preprocessing.py
    |-- src/utils/analysis.py
    `-- src/models/regression.py
    |
    v
Original AirQualityUCI dataset
```

## Module Responsibilities

`src/utils/data_loader.py`

- loads the raw CSV file
- handles semicolon separators and decimal commas
- drops empty rows and columns caused by trailing separators
- parses `Date` and `Time` into a timestamp
- converts `-200` sentinel values into missing values

`src/utils/preprocessing.py`

- creates temporal features
- builds leakage-aware feature matrices
- excludes other reference analyzer targets from model features
- performs chronological train/test splitting
- reports missingness

`src/utils/analysis.py`

- creates dataset-level summary metadata
- computes descriptive statistics
- computes sensor/reference correlations; Pearson is the default method, and Spearman can be used in the dashboard for rank-based monotonic relationships
- aggregates missing values by month

`src/models/regression.py`

- defines baseline and non-linear regression models
- uses median imputation inside scikit-learn pipelines
- evaluates models with chronological holdout metrics
- uses `TimeSeriesSplit` for cross-validation on the training period

## Data Workflow

```text
Raw CSV
  -> parse separator/decimal format
  -> parse timestamp
  -> convert -200 sentinel values
  -> inspect missingness
  -> create temporal features
  -> build sensor calibration feature matrix
  -> chronological split
  -> train regression models
  -> evaluate with MAE, RMSE, and R2
```

## Machine Learning Design

The workflow is regression-oriented because the dataset contains continuous gas concentration references. The default target is `C6H6(GT)`, but the app supports `CO(GT)`, `NOx(GT)`, and `NO2(GT)`.

The current feature set includes:

- metal oxide sensor responses
- temperature
- relative humidity
- absolute humidity
- cyclic hour and month features
- day-of-week feature

The feature set intentionally excludes the other reference analyzer concentrations. Including them could produce a stronger numerical score, but it would weaken the sensor calibration interpretation because those signals are ground-truth measurements from a certified analyzer.

## Model Preprocessing and Model Families

All models use median imputation for missing feature values through `SimpleImputer(strategy="median")`. Rows with a missing target are excluded before model fitting.

The benchmark uses four model families:

- `DummyRegressor`: median baseline used as the minimum reference performance.
- `Ridge`: regularized linear regression with median imputation and `StandardScaler`.
- `RandomForestRegressor`: tree-based ensemble with median imputation and no feature scaling.
- `GradientBoostingRegressor`: sequential tree-based ensemble with median imputation and no feature scaling.

`StandardScaler` is applied only to the Ridge model because linear models are sensitive to feature scale. Min-max normalization is not used. The tree-based models do not require standardization in the same way, so they are kept in their original measurement scale after imputation.

## Evaluation Strategy

The project uses:

- chronological holdout split
- time-series cross-validation on the training partition
- MAE, RMSE, and R2
- a dummy median regressor baseline
- Ridge regression, random forest regression, and gradient boosting regression as baseline model families

This is stronger than a random train/test split for a dataset with temporal drift. It is still a baseline strategy, not a full drift-aware scientific evaluation.

## Possible Extensions

The project could be extended with a database and API layer for near real-time sensor workflows. A realistic next step would be to store measurements and model outputs in PostgreSQL, expose ingestion and prediction endpoints through an API, and connect the system to deployed sensors or external air-quality services. Operational improvements would include scheduled data-quality checks, drift monitoring, model versioning, and prediction intervals for scientific interpretation.

## Scientific Limitations

The dataset is known to contain:

- cross-sensitivity between chemical sensors and gases
- concept drift
- sensor drift
- missing values encoded as `-200`

The current project acknowledges these issues but does not fully solve them. Missing values are handled through median imputation in model pipelines. Drift is partially addressed through chronological evaluation, but there is no explicit drift correction, calibration transfer method, or uncertainty quantification.

## Engineering Notes

The core analysis and ML code is kept outside Streamlit pages. This makes it easier to test and reuse. The Streamlit dashboard is a presentation and interaction layer, not the only place where the analysis logic exists.

## What This Project Demonstrates

- practical Python data cleaning
- tabular regression workflow
- leakage-aware feature selection
- time-aware evaluation
- separation between UI and analysis code
- documentation of scientific assumptions and limits

## What It Does Not Demonstrate

- operational model monitoring
- deployment-grade observability
- advanced drift correction
- uncertainty modelling
- real-time data ingestion
- scientific publication-level validation
