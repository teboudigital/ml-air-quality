from pathlib import Path

import streamlit as st

from src.ui.theme import apply_theme

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = PROJECT_ROOT / "docs"
SPHINX_HTML_DIR = DOCS_DIR / "build" / "html"
SPHINX_INDEX = DOCS_DIR / "build" / "html" / "index.html"
SPHINX_HTML_DIR_RELATIVE = Path("docs") / "build" / "html"
SPHINX_INDEX_RELATIVE = SPHINX_HTML_DIR_RELATIVE / "index.html"
REMOTE_DOCS_URL = "https://ml-air-quality-docs.onrender.com"


def as_posix_path(path: Path) -> str:
    """Return a stable repository-relative path for display and deployment docs."""
    return path.as_posix()


st.set_page_config(page_title="Documentation", layout="wide")
apply_theme()
st.title("Documentation")
st.markdown(
    """
    <style>
    button[data-testid="stBaseButton-secondary"] {
        background: #0E4548 !important;
        border: 1px solid #0E4548 !important;
        color: #FFFFFF !important;
    }

    button[data-testid="stBaseButton-secondary"] * {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
    }

    button[data-testid="stBaseButton-secondary"]:hover {
        background: #173C3B !important;
        border-color: #173C3B !important;
    }

    button[data-testid="stBaseButton-secondary"]:hover * {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
    }

    .aq-docs-link {
        display: inline-block;
        background: #0E4548;
        border: 1px solid #0E4548;
        color: #FFFFFF !important;
        text-decoration: none !important;
        font-weight: 700;
        border-radius: 8px;
        padding: 0.55rem 0.95rem;
    }

    .aq-docs-link:hover {
        background: #173C3B;
        border-color: #173C3B;
        color: #FFFFFF !important;
        text-decoration: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.write(
    "This page summarizes the project documentation available in the repository. "
    "The Streamlit dashboard remains the interactive analysis interface; Sphinx provides the structured technical and API documentation."
)

st.subheader("Repository Documentation")
docs = [
    {
        "Document": "README.md",
        "Purpose": "Project overview, installation, dashboard execution, tests, notebooks, and interview positioning.",
        "Path": "README.md",
    },
    {
        "Document": "docs/WORKFLOW.md",
        "Purpose": "Development workflow, reproducibility rules, testing, data handling, modelling rules, and pre-commit checklist.",
        "Path": "docs/WORKFLOW.md",
    },
    {
        "Document": "docs/TECHNICAL_ARCHITECTURE.md",
        "Purpose": "Architecture, data flow, module responsibilities, model design, evaluation strategy, and scientific limitations.",
        "Path": "docs/TECHNICAL_ARCHITECTURE.md",
    },
    {
        "Document": "docs/air_quality_analysis_ml.ipynb",
        "Purpose": "Reproducible exploratory data analysis and regression benchmark notebook.",
        "Path": "docs/air_quality_analysis_ml.ipynb",
    },
    {
        "Document": "docs/air_quality_analysis_ml_it.ipynb",
        "Purpose": "Italian explanatory notebook with variable descriptions and graph interpretation.",
        "Path": "docs/air_quality_analysis_ml_it.ipynb",
    },
]
st.dataframe(docs, use_container_width=True, hide_index=True)

st.subheader("Sphinx Documentation")
st.markdown(
    """
The project includes a lightweight Sphinx setup under `docs/source/`.

It contains:

- workflow documentation
- architecture documentation
- Python API reference generated from `src/`
"""
)

st.code("python -m sphinx -b html docs/source docs/build/html", language="bash")

st.markdown(
    f'<a class="aq-docs-link" href="{REMOTE_DOCS_URL}" target="_blank">Open deployed Sphinx documentation</a>',
    unsafe_allow_html=True,
)

if SPHINX_INDEX.exists():
    st.success("Sphinx HTML documentation has already been built.")
    st.info("The dashboard links to the deployed static Sphinx site instead of trying to start a local server.")
    st.write("Repository-relative path:")
    st.code(as_posix_path(SPHINX_INDEX_RELATIVE), language="text")
else:
    st.warning("Sphinx HTML documentation has not been built yet.")
    st.write("Run the build command above from the repository root to regenerate the static site contents:")
    st.code(as_posix_path(SPHINX_INDEX_RELATIVE), language="text")

with st.expander("How to use the documentation during a technical interview"):
    st.markdown(
        """
- Use `README.md` for the short project story and setup commands.
- Use `docs/WORKFLOW.md` to explain engineering discipline and reproducibility.
- Use `docs/TECHNICAL_ARCHITECTURE.md` to explain architecture and modelling decisions.
- Use Sphinx API docs to show that the reusable Python modules are documented separately from the Streamlit UI.
- Use the notebooks to explain the data-analysis reasoning step by step.
"""
    )

with st.expander("Why Sphinx is useful here"):
    st.markdown(
        """
Sphinx is useful because this project is not only a dashboard. It also contains reusable Python modules for data loading, preprocessing, analysis, metadata, and regression.

For a scientific software engineering role, this shows that the code can be inspected as an API, not only used through the graphical interface.
"""
    )
