import streamlit as st

from src.config import DEFAULT_TARGET, SUPPORTED_TARGETS
from src.models.regression import evaluate_models
from src.ui.theme import apply_theme
from src.utils.data_loader import load_air_quality_data


st.set_page_config(page_title="Regression Modeling", layout="wide")
apply_theme()
st.title("Regression Modeling")
st.markdown(
    """
    <style>
    button[data-testid="stBaseButton-primary"] {
        background: #0E4548 !important;
        border: 1px solid #0E4548 !important;
        color: #FFFFFF !important;
    }

    button[data-testid="stBaseButton-primary"] * {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
    }

    button[data-testid="stBaseButton-primary"]:hover {
        background: #173C3B !important;
        border-color: #173C3B !important;
    }

    button[data-testid="stBaseButton-primary"]:hover * {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

df = load_air_quality_data()

target = st.selectbox("Reference target", SUPPORTED_TARGETS, index=SUPPORTED_TARGETS.index(DEFAULT_TARGET))
test_size = st.slider("Chronological holdout size", min_value=0.1, max_value=0.4, value=0.2, step=0.05)
cv_splits = st.slider("Time-series CV splits", min_value=3, max_value=8, value=5, step=1)

if st.button("Run regression benchmark", type="primary"):
    with st.spinner("Training regression models with chronological evaluation..."):
        run = evaluate_models(df, target=target, test_size=test_size, cv_splits=cv_splits)

    st.subheader("Leaderboard")
    st.dataframe(run.leaderboard, use_container_width=True)
    with st.expander("How to interpret the model leaderboard"):
        st.markdown(
            """
The leaderboard compares regression models on the selected pollutant target.

- **Dummy median** is the baseline model.
- **Ridge** is a regularized linear regression model.
- **Random forest** is a tree-based ensemble model.
- **Gradient boosting** is a sequential tree-based ensemble model.
- **MAE** is the average absolute prediction error in the same unit as the target.
- **RMSE** penalizes larger errors more strongly than MAE.
- **R2** measures how much variance is explained by the model. Higher is better, but negative values can happen when the model is worse than a simple baseline.
- The **Dummy median** model is a baseline. A useful model should beat it.

The holdout split is chronological, so the model is trained on earlier observations and evaluated on later observations. This is more realistic than a random split for a drifting sensor dataset.
"""
        )

    cols = st.columns(3)
    cols[0].metric("Best model", run.best_model_name)
    cols[1].metric("Training rows", f"{run.train_rows:,}")
    cols[2].metric("Holdout rows", f"{run.test_rows:,}")

    st.subheader("Feature Set")
    st.write(", ".join(run.feature_columns))
    with st.expander("How to interpret the feature set"):
        st.markdown(
            """
The feature set includes sensor responses, weather variables, and temporal features.

It intentionally excludes the other `GT` reference-analyzer gas concentrations. This avoids an overly easy modelling setup where one certified analyzer measurement helps predict another certified analyzer measurement. For an interview, this is important: the project is closer to sensor calibration, not only numerical score optimization.
"""
        )

    st.info(
        "The benchmark intentionally excludes other reference analyzer gas concentrations from the feature matrix. "
        "This keeps the task closer to sensor calibration instead of leaking ground-truth laboratory signals."
    )
else:
    st.write("Choose a target and run the benchmark to compare regression models.")
