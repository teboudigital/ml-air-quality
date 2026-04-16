from pathlib import Path
import os
import socket
import subprocess
import sys

import streamlit as st

from src.config import ENGLISH_DASHBOARD_URL, ITALIAN_DASHBOARD_URL, SPHINX_DOCS_URL
from src.ui.theme import apply_theme

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = PROJECT_ROOT / "docs"
SPHINX_HTML_DIR = DOCS_DIR / "build" / "html"
SPHINX_INDEX = DOCS_DIR / "build" / "html" / "index.html"
SPHINX_HTML_DIR_RELATIVE = Path("docs") / "build" / "html"
SPHINX_INDEX_RELATIVE = SPHINX_HTML_DIR_RELATIVE / "index.html"
DOCS_PORT = 8765
DOCS_URL = f"http://localhost:{DOCS_PORT}"
IS_RENDER = os.getenv("RENDER", "").lower() == "true"


def as_posix_path(path: Path) -> str:
    """Return a stable repository-relative path for display and deployment docs."""
    return path.as_posix()


def is_port_open(host: str = "localhost", port: int = DOCS_PORT) -> bool:
    """Return True when a local documentation server is already reachable."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.3)
        return sock.connect_ex((host, port)) == 0


def start_docs_server() -> None:
    """Start a local static file server for the generated Sphinx HTML docs."""
    subprocess.Popen(
        [sys.executable, "-m", "http.server", str(DOCS_PORT), "--directory", str(SPHINX_HTML_DIR)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0,
    )


st.set_page_config(page_title="Documentation", layout="wide")
apply_theme()
st.title("Documentation")

st.write(
    "This page summarizes the project documentation available in the repository. "
    "The Streamlit dashboard remains the interactive analysis interface; Sphinx provides the structured technical and API documentation."
)

st.subheader("Online Deployments")
deployment_cols = st.columns(3)
deployment_cols[0].link_button("English dashboard", ENGLISH_DASHBOARD_URL)
deployment_cols[1].link_button("Italian dashboard", ITALIAN_DASHBOARD_URL)
deployment_cols[2].link_button("Sphinx documentation", SPHINX_DOCS_URL)

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

if SPHINX_INDEX.exists():
    st.success("Sphinx HTML documentation has already been built.")

    if IS_RENDER:
        st.link_button("Open deployed Sphinx documentation", SPHINX_DOCS_URL)
    else:
        if st.button("Start local documentation server"):
            if is_port_open():
                st.info(f"Documentation server is already running at {DOCS_URL}.")
            else:
                start_docs_server()
                st.success(f"Documentation server started at {DOCS_URL}.")

        if is_port_open():
            st.link_button("Open Sphinx documentation", DOCS_URL)
        else:
            st.info("Start the local documentation server, then use the link button.")

    st.write("Repository-relative path:")
    st.code(as_posix_path(SPHINX_INDEX_RELATIVE), language="text")
else:
    st.warning("Sphinx HTML documentation has not been built yet.")
    st.write("Run the build command above from the repository root, then open:")
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
