import plotly.express as px
import streamlit as st

from src.ui.theme import apply_theme, themed_plotly
from src.utils.analysis import build_dataset_profile, monthly_missingness, numeric_summary, variable_type_summary
from src.utils.data_loader import load_air_quality_data, summarize_data_quality
from src.utils.metadata import variable_dictionary
from src.utils.preprocessing import missingness_table


st.set_page_config(page_title="Data Overview", layout="wide")
apply_theme()
st.title("Data Overview")

df = load_air_quality_data()
profile = build_dataset_profile(df)
quality = summarize_data_quality()

cols = st.columns(4)
cols[0].metric("Rows", f"{profile.rows:,}")
cols[1].metric("Columns", profile.columns)
cols[2].metric("Raw -200 values", f"{quality.sentinel_values:,}")
cols[3].metric("Clean missing cells", f"{quality.missing_cells_after_cleaning:,}")

with st.expander("Dataset description and variable dictionary", expanded=False):
    st.markdown(
        """
The dataset contains hourly measurements from a chemical multisensor device deployed at road level in a polluted Italian city. The sensor array was co-located with a certified reference analyzer, which provides the `GT` ground-truth gas concentrations.

Important distinction:

- `GT` columns are reference analyzer concentrations.
- `PT08...` columns are raw metal oxide sensor responses. They are useful model inputs, but they are not certified pollutant concentrations.
- `NOx` means total nitrogen oxides. `NO2` means nitrogen dioxide. They are related but not identical.
- `CO` is carbon monoxide, `C6H6` is benzene, `NMHC` means non-methane hydrocarbons, and `O3` means ozone.
"""
    )
    st.dataframe(variable_dictionary(), use_container_width=True, hide_index=True)

st.subheader("Variables by Type")
type_summary = variable_type_summary(df)
chart_col, table_col = st.columns([2, 1])
with chart_col:
    st.plotly_chart(
        themed_plotly(
            px.pie(
                type_summary,
                names="variable_type",
                values="count",
                hole=0.45,
                title="Variable type distribution after preprocessing",
            )
        ),
        use_container_width=True,
    )
with table_col:
    st.dataframe(type_summary, use_container_width=True, hide_index=True)
with st.expander("How to read this chart"):
    st.markdown(
        """
This donut chart answers a basic data-analysis question: what kind of variables are available after cleaning?

- **Numerical** variables are sensor responses, gas reference concentrations, and weather variables. These are the variables used for regression.
- **Datetime** is the parsed timestamp created from the original `Date` and `Time` columns.
- **Categorical** variables do not appear after preprocessing because the original `Time` field is converted into a real timestamp and the measurements are continuous.

For this project, the result is expected: the dataset is mainly a numerical scientific time series, not a categorical survey dataset.
"""
    )

st.subheader("Missing Values")
missing = missingness_table(df)
st.dataframe(missing, use_container_width=True)

fig = px.bar(
    missing[missing["missing_values"] > 0],
    x="column",
    y="missing_percent",
    title="Missing values after converting -200 sentinels",
)
st.plotly_chart(themed_plotly(fig), use_container_width=True)
with st.expander("How to interpret missing values"):
    st.markdown(
        """
The original dataset uses `-200` to mark invalid or missing measurements. The app converts those values into missing values before analysis.

Large missing percentages mean that a variable is less reliable for modelling unless the missing-data strategy is explicit. `NMHC(GT)` is usually the most problematic reference variable, so it is not used as a default modelling target. Sensor variables and weather variables have fewer missing values, which makes them more useful for baseline regression.
"""
    )

st.subheader("Monthly Data Quality")
monthly = monthly_missingness(df)
st.plotly_chart(
    themed_plotly(px.line(monthly, x="month", y="missing_cells", markers=True)),
    use_container_width=True,
)
with st.expander("How to interpret monthly data quality"):
    st.markdown(
        """
This line chart shows whether missing data is concentrated in specific months.

If one month has many more missing cells, model performance for that period may be less reliable. In a research interview, this is a good place to mention that missingness is not only a cleaning issue: it can also reveal instrument downtime, calibration problems, or data acquisition issues.
"""
    )

st.subheader("Numeric Summary")
st.dataframe(numeric_summary(df), use_container_width=True)
with st.expander("How to interpret numeric summary"):
    st.markdown(
        """
The numeric summary gives the range, mean, median, and spread of each measurement.

Use it to identify outliers, very skewed variables, and columns with very different units. For example, `CO(GT)` is measured in mg/m^3, while `NO2(GT)` is measured in microg/m^3. Comparing raw numbers across different units is not meaningful unless the units are considered.
"""
    )
