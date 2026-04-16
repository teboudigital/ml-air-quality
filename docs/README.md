# Documentation

This folder contains the project documentation for the Air Quality Sensor Calibration Dashboard.

Main documents:

- `TECHNICAL_ARCHITECTURE.md`: architecture, data flow, modelling workflow, and scientific limitations.
- `WORKFLOW.md`: development workflow, reproducibility rules, testing, and extension guidelines.
- `air_quality_analysis_ml.ipynb`: reproducible EDA and regression notebook.
- `air_quality_analysis_ml_it.ipynb`: Italian explanatory notebook with variable descriptions and graph interpretation.
- `source/`: Sphinx source documentation for workflow, architecture, and Python API reference.

The documentation is intentionally written in English because the project is meant for portfolio and interview use.

Build Sphinx docs from the repository root:

```powershell
sphinx-build -b html docs/source docs/build/html
```
