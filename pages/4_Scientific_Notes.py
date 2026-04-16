import streamlit as st

from src.ui.theme import apply_theme

st.set_page_config(page_title="Scientific Notes", layout="wide")
apply_theme()
st.title("Scientific Notes")

st.subheader("Dataset Context")
st.write(
    "This dataset contains hourly measurements collected by a chemical multisensor device deployed at road level "
    "in an Italian urban area. Sensor responses are recorded together with certified reference analyzer "
    "measurements for several pollutants. The analysis therefore treats the problem as a sensor calibration and "
    "regression task, not as a classification task."
)

st.subheader("Scientific Assumptions")
st.markdown(
    """
- `-200` values are invalid measurements and are treated as missing data.
- `GT` columns represent certified reference analyzer concentrations.
- `PT08...` columns represent raw metal oxide sensor responses, not certified pollutant concentrations.
- Temperature and humidity are included because environmental conditions can affect chemical sensor responses.
- Chronological evaluation is used because the dataset is time ordered and may contain sensor drift or concept drift.
"""
)

st.subheader("Interpretation of Air Quality")
st.markdown(
    """
- Lower `CO(GT)`, `C6H6(GT)`, `NOx(GT)`, and `NO2(GT)` generally indicate cleaner conditions for the measured pollutants.
- Higher `CO(GT)`, `C6H6(GT)`, `NOx(GT)`, and `NO2(GT)` generally indicate more polluted episodes.
- `NOx(GT)` represents total nitrogen oxides, while `NO2(GT)` represents nitrogen dioxide specifically.
- `C6H6(GT)` represents benzene, a pollutant of interest for sensor calibration in this dataset.
- These values should be read together with time, humidity, temperature, and missing-data patterns.

This interpretation is qualitative. The dashboard does not certify legal air-quality compliance because official assessment depends on pollutant-specific averaging windows, validated regulatory procedures, and current threshold values.
"""
)

st.subheader("Modelling Methods")
st.markdown(
    """
All models are evaluated as **regression models**. The goal is to estimate a continuous pollutant concentration, not to classify observations into categories.

Common preprocessing:

- Rows with a missing target value are excluded from modelling.
- Missing feature values are handled with `SimpleImputer(strategy="median")`.
- The feature set includes sensor responses, meteorological variables, and temporal features.
- Other `GT` reference gas concentrations are excluded from the feature matrix to reduce target leakage.
- Evaluation uses a chronological holdout split and time-series cross-validation.

Model-specific choices:

| Model | Preprocessing | Why it is used | Main limitation |
|---|---|---|---|
| `DummyRegressor` | Median imputation | Baseline model. It predicts a simple central value and shows the minimum performance to beat. | It does not learn sensor relationships. |
| `Ridge` | Median imputation + `StandardScaler` | Regularized linear regression. Useful to test whether a simple linear calibration is already informative. | It may miss non-linear sensor behaviour. |
| `RandomForestRegressor` | Median imputation, no scaling | Tree-based ensemble. Useful for non-linear relationships and feature interactions. | It can be less transparent and may overfit if not controlled. |
| `GradientBoostingRegressor` | Median imputation, no scaling | Sequential tree-based ensemble. Useful for stronger non-linear regression baselines. | It still does not explicitly model sensor drift or uncertainty. |

`StandardScaler` is used only for `Ridge`, because linear models are sensitive to feature scale. The tree-based models do not require standardization in the same way, so no min-max normalization is applied.
"""
)

st.subheader("Methodological Limits")
st.markdown(
    """
- The modelling task is tabular regression, not classification.
- The benchmark provides baseline regression models, not a full atmospheric chemistry model.
- Drift is considered through chronological evaluation, but no explicit drift-correction algorithm is implemented.
- Prediction uncertainty is not estimated.
- The app does not simulate real-time deployment, sensor maintenance, or model monitoring.
"""
)

st.subheader("Possible Extensions")
st.markdown(
    """
- Connect the application to a database such as PostgreSQL to store measurements, model outputs, and data-quality checks.
- Add an API layer to receive measurements from external services or deployed sensor devices.
- Support near real-time ingestion from air-quality sensors instead of using only a static historical CSV file.
- Add scheduled validation jobs to monitor missing values, sensor drift, and prediction error over time.
- Store trained model artifacts and evaluation reports with versioning.
- Add uncertainty estimates or prediction intervals for scientific interpretation.
- Compare more advanced drift-aware calibration strategies against the current baseline models.
"""
)

st.subheader("Summary")
st.markdown(
    """
The project provides a reproducible baseline workflow for noisy air-quality sensor data: loading, cleaning, missing-value handling, exploratory analysis, leakage-aware feature construction, and regression evaluation. Its strongest scientific value is the explicit treatment of sensor responses as noisy calibration inputs rather than direct pollutant measurements.
"""
)
