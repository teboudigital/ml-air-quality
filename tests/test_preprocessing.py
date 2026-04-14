from src.config import DEFAULT_TARGET
from src.utils.data_loader import load_air_quality_data
from src.utils.preprocessing import add_time_features, build_modeling_frame, chronological_train_test_split


def test_add_time_features_creates_cyclic_columns():
    df = load_air_quality_data()
    engineered = add_time_features(df)

    assert "hour_sin" in engineered.columns
    assert "hour_cos" in engineered.columns
    assert "month_sin" in engineered.columns
    assert "month_cos" in engineered.columns


def test_build_modeling_frame_excludes_reference_leakage_columns():
    df = load_air_quality_data()
    X, y = build_modeling_frame(df, DEFAULT_TARGET)

    assert DEFAULT_TARGET not in X.columns
    assert "CO(GT)" not in X.columns
    assert "NOx(GT)" not in X.columns
    assert len(X) == len(y)
    assert y.notna().all()


def test_chronological_train_test_split_preserves_row_order():
    df = load_air_quality_data()
    X, y = build_modeling_frame(df, DEFAULT_TARGET)
    X_train, X_test, y_train, y_test = chronological_train_test_split(X, y, test_size=0.2)

    assert len(X_train) > len(X_test)
    assert X_train.index.max() < X_test.index.min()
    assert len(y_train) == len(X_train)
    assert len(y_test) == len(X_test)
