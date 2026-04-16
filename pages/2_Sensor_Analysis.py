import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.config import REFERENCE_COLUMNS, SENSOR_COLUMNS
from src.ui.theme import COLORS, apply_theme, themed_plotly
from src.utils.analysis import correlation_adjacency_matrix, correlation_edge_list, correlation_p_values, sensor_reference_correlation
from src.utils.data_loader import load_air_quality_data


st.set_page_config(page_title="Sensor Analysis", layout="wide")
apply_theme()
st.title("Sensor Analysis")

df = load_air_quality_data()

sensor = st.selectbox("Sensor response", [col for col in SENSOR_COLUMNS if col in df.columns])
target = st.selectbox("Reference analyzer target", [col for col in REFERENCE_COLUMNS if col in df.columns], index=2)

st.subheader("Temporal Behaviour")
st.plotly_chart(
    themed_plotly(px.line(df, x="timestamp", y=[sensor, target], title=f"{sensor} and {target} over time")),
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
            line={"color": COLORS["warning"], "width": 2},
        )
    )
st.plotly_chart(themed_plotly(fig), use_container_width=True)
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
    themed_plotly(
        px.imshow(
            corr,
            text_auto=".2f",
            aspect="auto",
            title=f"{correlation_method.title()} correlation matrix: sensors and reference gases",
            color_continuous_scale=["#B65B4B", "#F5F8F6", "#0E4548"],
        )
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

st.subheader("Adjacency Matrix and Correlation Network")
threshold_col, alpha_col = st.columns(2)
with threshold_col:
    correlation_threshold = st.selectbox(
        "Minimum absolute correlation threshold",
        [0.30, 0.50, 0.70, 0.80, 0.90],
        index=2,
        help="Common rule-of-thumb values: 0.30 weak/moderate, 0.50 moderate, 0.70 strong, 0.80 very strong, 0.90 extremely strong.",
    )
with alpha_col:
    alpha = st.selectbox(
        "Maximum p-value alpha",
        [0.10, 0.05, 0.01, 0.001],
        index=1,
        help="Common significance levels. 0.05 is the standard default; 0.01 and 0.001 are stricter.",
    )

p_values = correlation_p_values(df, method=correlation_method)
adjacency = correlation_adjacency_matrix(
    correlation=corr,
    p_values=p_values,
    correlation_threshold=correlation_threshold,
    alpha=alpha,
)
edges = correlation_edge_list(corr, adjacency)

st.write(
    f"An edge is kept when `abs(correlation) >= {correlation_threshold}` and `p-value <= {alpha}`."
)
styled_adjacency = adjacency.style.map(
    lambda value: (
        f"background-color: {COLORS['accent']}; color: {COLORS['ink']}; font-weight: 600"
        if value == 1
        else f"background-color: {COLORS['paper']}; color: {COLORS['ink']}; font-weight: 500"
    )
)
st.dataframe(styled_adjacency, use_container_width=True)

if edges.empty:
    st.warning("No edges match the selected correlation and p-value thresholds.")
else:
    display_edges = edges.copy()
    display_edges["relationship"] = display_edges["source"] + " -- " + display_edges["target"]
    display_edges["sign"] = np.where(display_edges["correlation"] >= 0, "positive", "negative")
    st.dataframe(display_edges, use_container_width=True, hide_index=True)

    nodes = list(adjacency.columns)
    angles = np.linspace(0, 2 * np.pi, len(nodes), endpoint=False)
    positions = {node: (np.cos(angle), np.sin(angle)) for node, angle in zip(nodes, angles)}

    node_x = [positions[node][0] for node in nodes]
    node_y = [positions[node][1] for node in nodes]
    node_degree = [int(adjacency.loc[node].sum()) for node in nodes]

    network_fig = go.Figure()
    edge_x = []
    edge_y = []
    for _, edge in edges.iterrows():
        x0, y0 = positions[edge["source"]]
        x1, y1 = positions[edge["target"]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    network_fig.add_trace(
        go.Scatter(
            x=edge_x,
            y=edge_y,
            mode="lines",
            line={"width": 1, "color": COLORS["line"]},
            hoverinfo="none",
            name="Significant correlation",
        )
    )
    network_fig.add_trace(
        go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text",
            text=nodes,
            textposition="top center",
            marker={
                "size": [12 + degree * 2 for degree in node_degree],
                "color": node_degree,
                "colorscale": [[0, COLORS["panel"]], [0.5, COLORS["accent"]], [1, COLORS["deep"]]],
                "showscale": True,
                "colorbar": {"title": "Degree"},
            },
            hovertemplate="<b>%{text}</b><br>Connections: %{marker.color}<extra></extra>",
            name="Variables",
        )
    )
    network_fig.update_layout(
        title="Correlation network graph filtered by threshold and p-value",
        showlegend=False,
        xaxis={"visible": False},
        yaxis={"visible": False},
        margin={"l": 10, "r": 10, "t": 50, "b": 10},
        height=650,
    )
    st.plotly_chart(themed_plotly(network_fig), use_container_width=True)

with st.expander("How to interpret the adjacency matrix and network graph"):
    st.markdown(
        f"""
The **threshold** is the minimum absolute correlation required to keep a relationship. Here it is set to `{correlation_threshold}`.

The **alpha value** is the maximum accepted p-value. Here it is set to `{alpha}`.

- `1` in the adjacency matrix means the relationship is kept.
- `0` means the relationship is filtered out.
- A node is a variable.
- An edge is a relationship that passes both filters: `abs(correlation) >= threshold` and `p-value <= alpha`.
- Larger or more intensely colored nodes have more retained connections.

The table uses `source` and `target` to identify each variable pair, but the network is **undirected**. Correlation does not prove causal direction, so arrows are intentionally not drawn.

Because this dataset has many hourly observations, p-values can become very small even for relationships that are not scientifically strong. For that reason, the graph uses both statistical significance and correlation strength.
"""
    )
