import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.config import REFERENCE_COLUMNS, SENSOR_COLUMNS
from src.utils.analysis import sensor_reference_correlation
from src.utils.data_loader import load_air_quality_data


st.set_page_config(page_title="Sensor Analysis", layout="wide")
st.title("Sensor Analysis")

df = load_air_quality_data()

sensor = st.selectbox("Sensor response", [col for col in SENSOR_COLUMNS if col in df.columns])
target = st.selectbox("Reference analyzer target", [col for col in REFERENCE_COLUMNS if col in df.columns], index=2)

st.subheader("Temporal Behaviour")
st.plotly_chart(
    px.line(df, x="timestamp", y=[sensor, target], title=f"{sensor} and {target} over time"),
    use_container_width=True,
)
with st.expander("How to interpret this time-series chart"):
    st.markdown(
        """
This chart compares a raw sensor response with a certified reference concentration over time.

- If both lines rise and fall together, the selected sensor is probably informative for that gas.
- If the relationship changes across months, that can indicate sensor drift, seasonality, or changing environmental conditions.
- A cleaner period is usually associated with lower reference concentrations, especially for `CO(GT)`, `C6H6(GT)`, `NOx(GT)`, and `NO2(GT)`.

This chart should not be used as a legal air-quality classification. The data is historical, hourly, and the app does not compute official regulatory averages.
"""
    )

st.subheader("Sensor vs Reference Target")
scatter_df = df[[sensor, target]].dropna()
fig = px.scatter(
    scatter_df,
    x=sensor,
    y=target,
    opacity=0.35,
    title="Relationship between field sensor response and certified reference measurement",
)
if len(scatter_df) >= 2:
    slope, intercept = np.polyfit(scatter_df[sensor], scatter_df[target], deg=1)
    x_line = np.array([scatter_df[sensor].min(), scatter_df[sensor].max()])
    y_line = slope * x_line + intercept
    fig.add_trace(
        go.Scatter(
            x=x_line,
            y=y_line,
            mode="lines",
            name="Linear trend",
            line={"color": "#d62728", "width": 2},
        )
    )
st.plotly_chart(fig, use_container_width=True)
with st.expander("How to interpret this scatter plot"):
    st.markdown(
        """
Each point is one hourly observation. The x-axis is the selected sensor response, and the y-axis is the certified reference measurement.

- A clear upward or downward pattern means the sensor contains useful information for estimating the target gas.
- A wide cloud around the trend line means the sensor response is noisy or affected by other variables.
- Non-linear patterns suggest that simple linear calibration may be too weak.
- If the cloud changes shape at high concentrations, the sensor may respond differently during polluted episodes.

The red trend line is only a simple visual guide. It is not the final ML model.
"""
    )

st.subheader("Correlation Matrix")
correlation_method = st.selectbox("Correlation method", ["pearson", "spearman"], format_func=str.title)
corr = sensor_reference_correlation(df, method=correlation_method)
st.plotly_chart(
    px.imshow(
        corr,
        text_auto=".2f",
        aspect="auto",
        title=f"{correlation_method.title()} correlation matrix: sensors and reference gases",
    ),
    use_container_width=True,
)
with st.expander("How to interpret the correlation matrix"):
    st.markdown(
        f"""
This matrix uses the **{correlation_method.title()}** correlation method.

- **Pearson** measures linear relationships.
- **Spearman** measures monotonic relationships based on ranks and is less tied to strict linearity.
- Values close to `1` mean two variables tend to increase together.
- Values close to `-1` mean one variable tends to decrease when the other increases.
- Values close to `0` mean there is no strong relationship according to the selected method.

For scientific sensor data, correlation is only a first diagnostic. It does not prove causality, does not remove cross-sensitivity, and does not solve drift.
"""
    )

st.caption(
    f"{correlation_method.title()} correlation is descriptive only. It does not remove drift, cross-sensitivity, seasonality, or temporal leakage risk."
)
