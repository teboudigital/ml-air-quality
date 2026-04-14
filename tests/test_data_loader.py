import pandas as pd

from src.config import DATA_FILE
from src.utils.data_loader import load_air_quality_data, summarize_data_quality


def test_load_air_quality_data_parses_timestamp_and_missing_values():
    df = load_air_quality_data(DATA_FILE)

    assert "timestamp" in df.columns
    assert pd.api.types.is_datetime64_any_dtype(df["timestamp"])
    assert len(df) == 9357
    assert df.isna().sum().sum() > 0


def test_summarize_data_quality_counts_sentinel_values():
    summary = summarize_data_quality(DATA_FILE)

    assert summary.rows == 9357
    assert summary.sentinel_values > 0
    assert summary.missing_cells_after_cleaning == summary.sentinel_values
