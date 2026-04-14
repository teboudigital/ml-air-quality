from __future__ import annotations

import numpy as np
import pandas as pd

from src.config import METEO_COLUMNS, REFERENCE_COLUMNS, SENSOR_COLUMNS, SUPPORTED_TARGETS


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add cyclic and calendar features from the timestamp column."""
    if "timestamp" not in df.columns:
        raise ValueError("Expected a timestamp column before feature engineering.")

    engineered = df.copy()
    timestamp = pd.to_datetime(engineered["timestamp"])

    engineered["hour"] = timestamp.dt.hour
    engineered["month"] = timestamp.dt.month
    engineered["day_of_week"] = timestamp.dt.dayofweek
    engineered["hour_sin"] = np.sin(2 * np.pi * engineered["hour"] / 24)
    engineered["hour_cos"] = np.cos(2 * np.pi * engineered["hour"] / 24)
    engineered["month_sin"] = np.sin(2 * np.pi * engineered["month"] / 12)
    engineered["month_cos"] = np.cos(2 * np.pi * engineered["month"] / 12)

    return engineered


def build_modeling_frame(df: pd.DataFrame, target: str) -> tuple[pd.DataFrame, pd.Series]:
    """Build a leakage-aware feature matrix and target vector for sensor calibration."""
    if target not in SUPPORTED_TARGETS:
        raise ValueError(f"Unsupported target: {target}. Supported targets: {SUPPORTED_TARGETS}")

    engineered = add_time_features(df)
    candidate_features = SENSOR_COLUMNS + METEO_COLUMNS + [
        "hour_sin",
        "hour_cos",
        "month_sin",
        "month_cos",
        "day_of_week",
    ]
    feature_columns = [col for col in candidate_features if col in engineered.columns]

    modeling = engineered[feature_columns + [target]].dropna(subset=[target])
    X = modeling[feature_columns]
    y = modeling[target]
    return X, y


def chronological_train_test_split(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = 0.2,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Split the dataset chronologically to preserve the temporal structure."""
    if not 0 < test_size < 1:
        raise ValueError("test_size must be between 0 and 1.")
    if len(X) != len(y):
        raise ValueError("X and y must have the same number of rows.")

    split_index = int(len(X) * (1 - test_size))
    if split_index <= 0 or split_index >= len(X):
        raise ValueError("Not enough rows to create a chronological train/test split.")

    return X.iloc[:split_index], X.iloc[split_index:], y.iloc[:split_index], y.iloc[split_index:]


def missingness_table(df: pd.DataFrame) -> pd.DataFrame:
    """Return a sorted missing-value table."""
    missing = df.isna().sum()
    table = pd.DataFrame(
        {
            "column": missing.index,
            "missing_values": missing.values,
            "missing_percent": (missing.values / len(df)) * 100,
        }
    )
    return table.sort_values("missing_values", ascending=False).reset_index(drop=True)


def available_reference_columns(df: pd.DataFrame) -> list[str]:
    """Return reference analyzer columns available in the loaded dataset."""
    return [col for col in REFERENCE_COLUMNS if col in df.columns]
