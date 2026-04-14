from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from scipy import stats

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


def correlation_p_values(df: pd.DataFrame, method: str = "pearson") -> pd.DataFrame:
    """Compute pairwise p-values for Pearson or Spearman correlations."""
    columns = [col for col in SENSOR_COLUMNS + REFERENCE_COLUMNS if col in df.columns]
    p_values = pd.DataFrame(1.0, index=columns, columns=columns)

    for left_index, left in enumerate(columns):
        p_values.loc[left, left] = 0.0
        for right in columns[left_index + 1 :]:
            pair = df[[left, right]].dropna()
            if len(pair) < 3 or pair[left].nunique() < 2 or pair[right].nunique() < 2:
                p_value = 1.0
            elif method == "pearson":
                _, p_value = stats.pearsonr(pair[left], pair[right])
            elif method == "spearman":
                _, p_value = stats.spearmanr(pair[left], pair[right])
            else:
                raise ValueError("method must be 'pearson' or 'spearman'.")

            p_values.loc[left, right] = p_value
            p_values.loc[right, left] = p_value

    return p_values


def correlation_adjacency_matrix(
    correlation: pd.DataFrame,
    p_values: pd.DataFrame,
    correlation_threshold: float,
    alpha: float,
) -> pd.DataFrame:
    """Create an adjacency matrix from correlation strength and p-value filters."""
    adjacency = ((correlation.abs() >= correlation_threshold) & (p_values <= alpha)).astype(int)
    for column in adjacency.columns:
        adjacency.loc[column, column] = 0
    return adjacency


def correlation_edge_list(correlation: pd.DataFrame, adjacency: pd.DataFrame) -> pd.DataFrame:
    """Build an undirected edge list from an adjacency matrix."""
    rows = []
    columns = list(adjacency.columns)
    for left_index, left in enumerate(columns):
        for right in columns[left_index + 1 :]:
            if adjacency.loc[left, right] == 1:
                rows.append(
                    {
                        "source": left,
                        "target": right,
                        "correlation": correlation.loc[left, right],
                        "abs_correlation": abs(correlation.loc[left, right]),
                    }
                )
    return pd.DataFrame(rows).sort_values("abs_correlation", ascending=False).reset_index(drop=True)


def monthly_missingness(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate missing cells by month to make temporal data-quality issues visible."""
    work = df.copy()
    work["month"] = pd.to_datetime(work["timestamp"]).dt.to_period("M").astype(str)
    value_columns = [col for col in work.columns if col != "timestamp"]
    return work.groupby("month")[value_columns].apply(lambda frame: int(frame.isna().sum().sum())).reset_index(
        name="missing_cells"
    )
