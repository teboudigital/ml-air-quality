from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import numpy as np

from src.config import DATA_FILE, SENTINEL_MISSING_VALUE


@dataclass(frozen=True)
class DataQualitySummary:
    rows: int
    columns: int
    sentinel_values: int
    missing_cells_after_cleaning: int


def load_air_quality_data(path: Path | str = DATA_FILE) -> pd.DataFrame:
    """Load and normalize the original UCI Air Quality CSV file."""
    data_path = Path(path)
    if not data_path.exists():
        raise FileNotFoundError(f"Air quality data file not found: {data_path}")

    df = pd.read_csv(data_path, sep=";", decimal=",")
    df = df.dropna(axis=1, how="all")
    df = df.dropna(axis=0, how="all")
    df.columns = [str(col).strip() for col in df.columns]

    if "Date" not in df.columns or "Time" not in df.columns:
        raise ValueError("Expected Date and Time columns in the air quality dataset.")

    timestamp = pd.to_datetime(
        df["Date"].astype(str) + " " + df["Time"].astype(str).str.replace(".", ":", regex=False),
        dayfirst=True,
        errors="coerce",
    )
    df.insert(0, "timestamp", timestamp)
    df = df.drop(columns=["Date", "Time"])

    numeric_columns = df.columns.drop("timestamp")
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors="coerce")
    df[numeric_columns] = df[numeric_columns].replace(SENTINEL_MISSING_VALUE, np.nan).astype("float64")

    return df.sort_values("timestamp").reset_index(drop=True)


def summarize_data_quality(path: Path | str = DATA_FILE) -> DataQualitySummary:
    """Return a compact summary of raw sentinel values and cleaned missing cells."""
    raw = pd.read_csv(path, sep=";", decimal=",").dropna(axis=1, how="all").dropna(axis=0, how="all")
    sentinel_values = int((raw == SENTINEL_MISSING_VALUE).sum(numeric_only=True).sum())
    clean = load_air_quality_data(path)
    return DataQualitySummary(
        rows=len(clean),
        columns=len(clean.columns),
        sentinel_values=sentinel_values,
        missing_cells_after_cleaning=int(clean.isna().sum().sum()),
    )
