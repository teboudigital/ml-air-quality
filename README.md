# Applied ML Portfolio

Single-deployment Streamlit portfolio with a selector-first entry flow.

## Current Setup

- `app.py`: landing selector shown before entering any project
- `projects/air_quality`: standalone-style replica of the Air Quality Sensor Calibration app
- `render.yaml`: existing Render deployment entry kept in place

## Why This Structure

The portfolio should not switch live between projects inside the same active interface. Instead:

1. the user lands on a selector screen
2. the user chooses one project
3. the app enters that project as an isolated experience
4. changing project later means returning to the selector and starting over

This avoids cross-project state, cache, and reload problems inside Streamlit.

## Architecture

```text
app.py
projects/
  air_quality/
    app.py
    pages/
    src/
    docs/
    tests/
render.yaml
requirements.txt
```

## Local Run

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m streamlit run app.py
```

## Render

The current deployment entry remains:

```text
streamlit run app.py --server.headless true --server.port $PORT --server.address 0.0.0.0
```

## Notes

- `projects/air_quality` is intended to stay visually and functionally aligned with the standalone `ml-air-quality` repository.
- The root portfolio layer should stay minimal and should not restyle the project after entry.
