from pathlib import Path
import os


APP_TITLE = "Air Quality Sensor Calibration"
APP_TITLE_IT = "Calibrazione dei Sensori di Qualita dell'Aria"
RANDOM_STATE = 42
APP_LANGUAGE = os.getenv("APP_LANGUAGE", "en").lower()

ENGLISH_DASHBOARD_URL = os.getenv("ENGLISH_DASHBOARD_URL", "https://ml-air-quality.onrender.com")
ITALIAN_DASHBOARD_URL = os.getenv("ITALIAN_DASHBOARD_URL", "https://ml-air-quality-it.onrender.com")
SPHINX_DOCS_URL = os.getenv("SPHINX_DOCS_URL", "https://ml-air-quality-docs.onrender.com")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "src" / "data"
DATA_FILE = DATA_DIR / "AirQualityUCI.csv"

SENTINEL_MISSING_VALUE = -200

REFERENCE_COLUMNS = ["CO(GT)", "NMHC(GT)", "C6H6(GT)", "NOx(GT)", "NO2(GT)"]
SENSOR_COLUMNS = [
    "PT08.S1(CO)",
    "PT08.S2(NMHC)",
    "PT08.S3(NOx)",
    "PT08.S4(NO2)",
    "PT08.S5(O3)",
]
METEO_COLUMNS = ["T", "RH", "AH"]
DEFAULT_TARGET = "C6H6(GT)"
SUPPORTED_TARGETS = ["CO(GT)", "C6H6(GT)", "NOx(GT)", "NO2(GT)"]
