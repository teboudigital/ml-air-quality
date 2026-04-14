from src.config import DEFAULT_TARGET
from src.models.regression import evaluate_models, regression_metrics
from src.utils.data_loader import load_air_quality_data


def test_regression_metrics_returns_expected_keys():
    metrics = regression_metrics([1, 2, 3], [1, 2, 4])

    assert set(metrics) == {"MAE", "RMSE", "R2"}
    assert metrics["MAE"] > 0


def test_evaluate_models_returns_leaderboard_on_subset():
    df = load_air_quality_data().head(1200)
    run = evaluate_models(df, target=DEFAULT_TARGET, test_size=0.2, cv_splits=3)

    assert not run.leaderboard.empty
    assert "holdout_MAE" in run.leaderboard.columns
    assert run.best_model_name in set(run.leaderboard["model"])
