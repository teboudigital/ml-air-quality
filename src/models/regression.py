from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import TimeSeriesSplit, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.config import RANDOM_STATE
from src.utils.preprocessing import build_modeling_frame, chronological_train_test_split


@dataclass(frozen=True)
class ModelRun:
    target: str
    leaderboard: pd.DataFrame
    best_model_name: str
    feature_columns: list[str]
    train_rows: int
    test_rows: int


def make_regression_models() -> dict[str, Pipeline]:
    """Create a small model suite suitable for tabular regression baselines."""
    return {
        "Dummy median": Pipeline(
            [("imputer", SimpleImputer(strategy="median")), ("model", DummyRegressor(strategy="median"))]
        ),
        "Ridge": Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                ("model", Ridge(alpha=1.0)),
            ]
        ),
        "Random forest": Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                (
                    "model",
                    RandomForestRegressor(
                        n_estimators=120,
                        min_samples_leaf=4,
                        random_state=RANDOM_STATE,
                        n_jobs=1,
                    ),
                ),
            ]
        ),
        "Gradient boosting": Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                ("model", GradientBoostingRegressor(n_estimators=140, learning_rate=0.06, random_state=RANDOM_STATE)),
            ]
        ),
    }


def regression_metrics(y_true: pd.Series, y_pred: np.ndarray) -> dict[str, float]:
    """Compute standard regression metrics."""
    mse = mean_squared_error(y_true, y_pred)
    return {
        "MAE": mean_absolute_error(y_true, y_pred),
        "RMSE": float(np.sqrt(mse)),
        "R2": r2_score(y_true, y_pred),
    }


def evaluate_models(df: pd.DataFrame, target: str, test_size: float = 0.2, cv_splits: int = 5) -> ModelRun:
    """Train and evaluate regression models with chronological holdout and time-series CV."""
    X, y = build_modeling_frame(df, target)
    X_train, X_test, y_train, y_test = chronological_train_test_split(X, y, test_size=test_size)

    models = make_regression_models()
    cv = TimeSeriesSplit(n_splits=cv_splits)
    rows: list[dict[str, float | str]] = []

    for model_name, model in models.items():
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        holdout = regression_metrics(y_test, predictions)
        cv_result = cross_validate(
            model,
            X_train,
            y_train,
            cv=cv,
            scoring=("neg_mean_absolute_error", "r2"),
            n_jobs=1,
        )

        rows.append(
            {
                "model": model_name,
                "holdout_MAE": holdout["MAE"],
                "holdout_RMSE": holdout["RMSE"],
                "holdout_R2": holdout["R2"],
                "cv_MAE_mean": -cv_result["test_neg_mean_absolute_error"].mean(),
                "cv_MAE_std": cv_result["test_neg_mean_absolute_error"].std(),
                "cv_R2_mean": cv_result["test_r2"].mean(),
            }
        )

    leaderboard = pd.DataFrame(rows).sort_values("holdout_MAE", ascending=True).reset_index(drop=True)
    return ModelRun(
        target=target,
        leaderboard=leaderboard,
        best_model_name=str(leaderboard.iloc[0]["model"]),
        feature_columns=X.columns.tolist(),
        train_rows=len(X_train),
        test_rows=len(X_test),
    )
