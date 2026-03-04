import argparse
import json
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from backend.ml.model_registry import ModelRegistry

FEATURE_COLS = [
    "accuracy_rate",
    "avg_response_time",
    "attempt_count",
    "error_pattern",
    "concept_attempt_ratio",
]


def train(data_path: str, model_type: str = "xgboost"):
    df = pd.read_csv(data_path)
    X = df[FEATURE_COLS]
    y = df["mastery_score"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    if model_type == "lightgbm":
        model = LGBMRegressor(n_estimators=200, learning_rate=0.05, random_state=42)
    else:
        model = XGBRegressor(n_estimators=300, learning_rate=0.05, max_depth=6, random_state=42)

    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    metrics = {
        "mae": float(mean_absolute_error(y_test, preds)),
        "r2": float(r2_score(y_test, preds)),
        "model_type": model_type,
    }

    reg = ModelRegistry()
    version = reg.register(model, metrics, prefix="gap_detector")
    return version, metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, help="Path to training CSV")
    parser.add_argument("--model", default="xgboost", choices=["xgboost", "lightgbm"])
    args = parser.parse_args()

    version, metrics = train(args.data, args.model)
    print(json.dumps({"version": version, "metrics": metrics}, indent=2))
