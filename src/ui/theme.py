from __future__ import annotations

import base64
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

from src.config import PROJECT_ROOT


IMAGE_DIR = PROJECT_ROOT / "src" / "images"
LOGO_IMAGE = IMAGE_DIR / "logo.png"

COLORS = {
    "ink": "#173C3B",
    "deep": "#0E4548",
    "panel": "#D7E7DE",
    "mist": "#E6EEE9",
    "paper": "#F5F8F6",
    "line": "#A8C1B9",
    "white": "#FFFFFF",
    "accent": "#6F9B8E",
    "warning": "#B65B4B",
}

PLOTLY_SEQUENCE = [
    COLORS["deep"],
    COLORS["accent"],
    "#88B7AA",
    "#4E756E",
    COLORS["warning"],
]


def apply_theme() -> None:
    """Apply the presentation-inspired visual style to Streamlit pages."""
    st.markdown(
        f"""
        <style>
        :root {{
            --aq-ink: {COLORS["ink"]};
            --aq-deep: {COLORS["deep"]};
            --aq-panel: {COLORS["panel"]};
            --aq-mist: {COLORS["mist"]};
            --aq-paper: {COLORS["paper"]};
            --aq-line: {COLORS["line"]};
            --aq-white: {COLORS["white"]};
            --aq-accent: {COLORS["accent"]};
            --aq-warning: {COLORS["warning"]};
        }}

        .stApp {{
            background: var(--aq-white);
            color: #000000;
        }}

        .main .block-container {{
            background: var(--aq-white);
            color: #000000;
        }}

        h1, h2, h3, h4, h5, h6 {{
            color: #000000;
            letter-spacing: 0;
        }}

        p, li, label, span, div[data-testid="stMarkdownContainer"] {{
            color: #000000;
        }}

        h1 {{
            font-weight: 800;
        }}

        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, var(--aq-deep) 0%, #123E3F 100%);
        }}

        [data-testid="stSidebar"] * {{
            color: var(--aq-white);
        }}

        [data-testid="stMetric"] {{
            background: rgba(255, 255, 255, 0.72);
            border: 1px solid var(--aq-line);
            border-radius: 8px;
            padding: 0.85rem 1rem;
        }}

        [data-testid="stMetricLabel"] {{
            color: var(--aq-deep);
            font-weight: 700;
        }}

        div[data-testid="stExpander"] {{
            border: 1px solid var(--aq-line);
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.68);
        }}

        .stButton > button,
        .stDownloadButton > button,
        a[data-testid="stLinkButton"] {{
            border-radius: 8px;
            border: 1px solid var(--aq-deep);
            background: var(--aq-deep);
            color: var(--aq-white);
            font-weight: 700;
        }}

        .stButton > button:hover,
        .stDownloadButton > button:hover,
        a[data-testid="stLinkButton"]:hover {{
            border-color: var(--aq-ink);
            background: var(--aq-ink);
            color: var(--aq-white);
        }}

        [data-testid="stDataFrame"] {{
            border: 1px solid var(--aq-line);
            border-radius: 8px;
            overflow: hidden;
        }}

        code {{
            color: var(--aq-deep);
        }}

        .aq-logo {{
            display: flex;
            justify-content: flex-end;
            align-items: flex-start;
            padding-top: 0.35rem;
        }}

        .aq-logo img {{
            width: 72px;
            height: 72px;
            object-fit: contain;
            border-radius: 8px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def themed_plotly(fig: go.Figure) -> go.Figure:
    """Apply the dashboard palette to a Plotly figure."""
    fig.update_layout(
        colorway=PLOTLY_SEQUENCE,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.68)",
        font={"color": COLORS["ink"]},
        title={"font": {"color": COLORS["ink"]}},
        legend={"bgcolor": "rgba(255,255,255,0)"},
        margin={"l": 20, "r": 20, "t": 60, "b": 30},
    )
    fig.update_xaxes(gridcolor=COLORS["line"], zerolinecolor=COLORS["line"])
    fig.update_yaxes(gridcolor=COLORS["line"], zerolinecolor=COLORS["line"])
    return fig


def show_top_right_logo() -> None:
    """Render the compact project logo."""
    if LOGO_IMAGE.exists():
        encoded = base64.b64encode(LOGO_IMAGE.read_bytes()).decode("ascii")
        st.markdown(
            f"""
            <div class="aq-logo">
                <img src="data:image/png;base64,{encoded}" alt="Air Quality Sensor logo">
            </div>
            """,
            unsafe_allow_html=True,
        )
