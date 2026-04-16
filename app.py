import streamlit as st

from src.config import APP_LANGUAGE, APP_TITLE, APP_TITLE_IT, ENGLISH_DASHBOARD_URL, ITALIAN_DASHBOARD_URL, SPHINX_DOCS_URL
from src.ui.theme import apply_theme, show_top_right_logo
from src.utils.analysis import build_dataset_profile
from src.utils.data_loader import load_air_quality_data


IS_ITALIAN = APP_LANGUAGE == "it"
page_title = APP_TITLE_IT if IS_ITALIAN else APP_TITLE

st.set_page_config(page_title=page_title, page_icon="AQ", layout="wide")
apply_theme()

title_col, logo_col = st.columns([5, 1])
with title_col:
    st.title(page_title)
with logo_col:
    show_top_right_logo()

if IS_ITALIAN:
    st.write(
        "Dashboard orientata alla ricerca per esplorare dati rumorosi di sensori di qualita dell'aria, "
        "misure di analizzatori di riferimento e calibrazione dei sensori tramite regressione."
    )
else:
    st.write(
        "Research-oriented dashboard for exploring noisy air-quality sensor data, "
        "reference analyzer measurements, and regression-based sensor calibration."
    )

link_cols = st.columns(3)
link_cols[0].link_button("English app", ENGLISH_DASHBOARD_URL)
link_cols[1].link_button("Versione italiana", ITALIAN_DASHBOARD_URL)
link_cols[2].link_button("Sphinx docs", SPHINX_DOCS_URL)

df = load_air_quality_data()
profile = build_dataset_profile(df)

metric_cols = st.columns(4)
metric_cols[0].metric("Rows", f"{profile.rows:,}")
metric_cols[1].metric("Columns", profile.columns)
metric_cols[2].metric("Date range", f"{profile.start_date.date()} to {profile.end_date.date()}")
metric_cols[3].metric("Missing cells", f"{profile.missing_cells:,}")

st.subheader("Focus del progetto" if IS_ITALIAN else "Project Focus")
if IS_ITALIAN:
    st.write(
        "La dashboard tratta il dataset come un problema scientifico di regressione: le risposte dei sensori "
        "e le variabili meteorologiche sono usate per stimare le concentrazioni misurate da un analizzatore di riferimento certificato."
    )
    st.markdown(
        """
- I valori mancanti codificati come `-200` sono convertiti in veri valori mancanti.
- I modelli sono valutati con split cronologici e cross-validation per serie temporali.
- La pagina di modellazione riporta metriche di regressione, non accuratezza di classificazione.
- Limiti scientifici come drift del sensore e cross-sensitivity sono documentati esplicitamente.
"""
    )
else:
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

st.subheader("Anteprima dati" if IS_ITALIAN else "Data Preview")
st.dataframe(df.head(20), use_container_width=True)
