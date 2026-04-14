from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from src.config import REFERENCE_COLUMNS, SENSOR_COLUMNS


@dataclass(frozen=True)
class DatasetProfile:
    rows: int
    columns: int
    start_date: pd.Timestamp
    end_date: pd.Timestamp
    missing_cells: int


def build_dataset_profile(df: pd.DataFrame) -> DatasetProfile:
    """Build high-level dataset metadata for the dashboard."""
    return DatasetProfile(
        rows=len(df),
        columns=len(df.columns),
        start_date=pd.to_datetime(df["timestamp"]).min(),
        end_date=pd.to_datetime(df["timestamp"]).max(),
        missing_cells=int(df.isna().sum().sum()),
    )


def numeric_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return descriptive statistics for numeric columns."""
    return df.select_dtypes(include="number").describe().T


def variable_type_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Count variables by broad analytical dtype."""
    rows = []
    for column, dtype in df.dtypes.items():
        if pd.api.types.is_numeric_dtype(dtype):
            variable_type = "Numerical"
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            variable_type = "Datetime"
        elif pd.api.types.is_bool_dtype(dtype):
            variable_type = "Boolean"
        else:
            variable_type = "Categorical"
        rows.append({"column": column, "variable_type": variable_type, "dtype": str(dtype)})

    detail = pd.DataFrame(rows)
    return (
        detail.groupby("variable_type")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
        .reset_index(drop=True)
    )


def sensor_reference_correlation(df: pd.DataFrame, method: str = "pearson") -> pd.DataFrame:
    """Compute correlations between sensor responses and reference targets."""
    columns = [col for col in SENSOR_COLUMNS + REFERENCE_COLUMNS if col in df.columns]
    return df[columns].corr(method=method, numeric_only=True)


def monthly_missingness(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate missing cells by month to make temporal data-quality issues visible."""
    work = df.copy()
    work["month"] = pd.to_datetime(work["timestamp"]).dt.to_period("M").astype(str)
    value_columns = [col for col in work.columns if col != "timestamp"]
    return work.groupby("month")[value_columns].apply(lambda frame: int(frame.isna().sum().sum())).reset_index(
        name="missing_cells"
    )
