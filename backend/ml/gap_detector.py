from dataclasses import dataclass
from typing import List
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from backend.ml.model_registry import ModelRegistry


@dataclass
class FeatureRow:
    accuracy_rate: float
    avg_response_time: float
    attempt_count: float
    error_pattern: float
    concept_attempt_ratio: float


class GapDetector:
    def __init__(self) -> None:
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.registry = ModelRegistry()
        self.is_trained = False

    def train_bootstrap(self) -> None:
        X = np.array([
            [0.9, 2200, 8, 0.2, 0.4],
            [0.3, 8100, 7, 0.8, 0.2],
            [0.8, 1800, 6, 0.3, 0.5],
            [0.2, 9200, 9, 0.9, 0.1],
            [0.85, 2600, 8, 0.2, 0.45],
            [0.4, 7000, 7, 0.7, 0.2],
        ])
        y = np.array([0.92, 0.35, 0.88, 0.28, 0.84, 0.42])
        self.model.fit(X, y)
        self.is_trained = True

    def _load_or_bootstrap(self):
        try:
            self.model = self.registry.get_active_model()
            self.is_trained = True
        except Exception:
            if not self.is_trained:
                self.train_bootstrap()

    def predict_mastery(self, rows: List[FeatureRow]) -> float:
        self._load_or_bootstrap()
        X = np.array([
            [r.accuracy_rate, r.avg_response_time, r.attempt_count, r.error_pattern, r.concept_attempt_ratio]
            for r in rows
        ])
        preds = self.model.predict(X)
        return float(np.clip(np.mean(preds), 0.0, 1.0))
