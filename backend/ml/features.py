from collections import Counter
from typing import Iterable


def build_features(answer_rows: Iterable[dict]) -> dict:
    rows = list(answer_rows)
    if not rows:
        return {
            "accuracy_rate": 0.0,
            "avg_response_time": 0.0,
            "attempt_count": 0.0,
            "error_pattern": 0.0,
            "concept_attempt_ratio": 0.0,
        }

    total = len(rows)
    correct = sum(1 for r in rows if r.get("correct", False))
    avg_time = sum(float(r.get("response_time_ms", 0)) for r in rows) / total
    attempts = float(total)

    wrong_questions = [r.get("question_id", "") for r in rows if not r.get("correct", False)]
    error_repetition = 0.0
    if wrong_questions:
        c = Counter(wrong_questions)
        error_repetition = max(c.values()) / len(wrong_questions)

    concept_count = len(set(r.get("concept", "") for r in rows if r.get("concept")))
    concept_attempt_ratio = concept_count / total if total else 0.0

    return {
        "accuracy_rate": correct / total,
        "avg_response_time": avg_time,
        "attempt_count": attempts,
        "error_pattern": error_repetition,
        "concept_attempt_ratio": concept_attempt_ratio,
    }
