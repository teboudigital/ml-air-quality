import streamlit as st

from src.config import APP_TITLE
from src.utils.analysis import build_dataset_profile
from src.utils.data_loader import load_air_quality_data


st.set_page_config(page_title=APP_TITLE, page_icon="AQ", layout="wide")

st.title(APP_TITLE)
st.write(
    "Research-oriented dashboard for exploring noisy air-quality sensor data, "
    "reference analyzer measurements, and regression-based sensor calibration."
)

df = load_air_quality_data()
profile = build_dataset_profile(df)

metric_cols = st.columns(4)
metric_cols[0].metric("Rows", f"{profile.rows:,}")
metric_cols[1].metric("Columns", profile.columns)
metric_cols[2].metric("Date range", f"{profile.start_date.date()} to {profile.end_date.date()}")
metric_cols[3].metric("Missing cells", f"{profile.missing_cells:,}")

st.subheader("Project Focus")
st.write(
    "The dashboard treats the dataset as a scientific regression problem: sensor responses and "
    "meteorological variables are used to estimate gas concentrations measured by a certified reference analyzer."
)

st.markdown(
    """
- Missing values encoded as `-200` are converted to real missing values.
- Models are evaluated with chronological splits and time-series cross-validation.
- The modelling page reports regression metrics rather than classification accuracy.
- Scientific caveats such as sensor drift and cross-sensitivity are documented explicitly.
"""
)

st.subheader("Data Preview")
st.dataframe(df.head(20), use_container_width=True)
