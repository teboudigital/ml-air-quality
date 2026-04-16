# Air Quality Sensor Calibration Dashboard

Python data analysis and machine learning project built around the UCI Air Quality dataset.

The dataset contains hourly measurements from a field-deployed chemical multisensor device in a polluted Italian urban area, together with reference gas concentrations measured by a certified co-located analyzer. The project focuses on reproducible exploratory analysis, missing-value handling, sensor calibration, and regression modelling for air-quality targets.

This is not a production air-quality monitoring system. It is a research-oriented portfolio project designed to demonstrate how to structure a noisy scientific dataset into an inspectable analysis and modelling workflow.

## What the Project Does

- Loads the original semicolon-separated AirQualityUCI file with European decimal commas.
- Converts the `Date` and `Time` fields into a timestamp.
- Replaces the dataset sentinel value `-200` with missing values.
- Summarizes missingness across sensor and reference-analyzer columns.
- Builds temporal features from hourly measurements.
- Trains regression models for selected pollutant targets such as `CO(GT)`, `C6H6(GT)`, `NOx(GT)`, and `NO2(GT)`.
- Uses chronological holdout evaluation and time-series cross-validation to reduce leakage risk.
- Provides a Streamlit dashboard for dataset inspection, sensor behaviour, modelling results, and scientific limitations.
- Includes tests for loading, preprocessing, feature engineering, and model evaluation.

## Scientific Context

The original dataset contains 9,358 hourly records collected from March 2004 to February 2005. It includes responses from metal oxide chemical sensors, meteorological variables, and ground-truth pollutant concentrations from a certified reference analyzer.

Important scientific constraints:

- missing values are encoded as `-200`
- chemical sensors can show cross-sensitivity
- sensor drift and concept drift are expected
- the correct task is regression, not classification
- temporal evaluation is more appropriate than purely random splitting
- the dataset is for research purposes only and excludes commercial use

Reference: S. De Vito, E. Massera, M. Piga, L. Martinotto, G. Francia, "On field calibration of an electronic nose for benzene estimation in an urban pollution monitoring scenario", Sensors and Actuators B: Chemical, 2008.

## Project Structure

```text
ml-air-quality/
|-- app.py
|-- pages/
|-- src/
|   |-- config.py
|   |-- data/
|   |-- models/
|   `-- utils/
|-- tests/
|-- docs/
|-- requirements.txt
`-- render.yaml
```

## Installation

```powershell
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the Dashboard

```powershell
streamlit run app.py
```

Open `http://localhost:8501`.

## Run Tests

```powershell
pytest
```

## Development Workflow

The development and reproducibility workflow is documented in:

```text
docs/WORKFLOW.md
```

It covers environment setup, testing, data handling conventions, missing-value policy, feature engineering rules, model evaluation rules, and pre-commit checks.

## Sphinx Documentation

Build the local Sphinx documentation with:

```powershell
sphinx-build -b html docs/source docs/build/html
```

Open the generated documentation from:

```text
docs/build/html/index.html
```

## Notebook

The project includes a Jupyter notebook for reproducible EDA and model benchmarking:

```text
docs/air_quality_analysis_ml.ipynb
```

An Italian explanatory version is also available:

```text
docs/air_quality_analysis_ml_it.ipynb
```

## Interview Positioning

> I built a Python and Streamlit analysis project around a real air-quality multisensor dataset. The goal is to turn noisy hourly sensor readings and certified reference measurements into a reproducible regression workflow, with explicit handling of missing sentinel values, temporal features, chronological model evaluation, and documentation of sensor drift and scientific limitations.

What it demonstrates:

- structured Python project organization
- data cleaning for a real scientific dataset
- regression-oriented ML workflow
- leakage-aware evaluation choices
- documentation of assumptions and limitations
- testable non-UI modules

What it does not prove:

- deployment of a real monitoring system
- online model monitoring
- advanced drift correction
- uncertainty quantification
- production MLOps at scale

## License and Dataset Use

The dataset metadata states that it can be used exclusively for research purposes and that commercial purposes are excluded. Keep that constraint visible if you publish or deploy this project.
