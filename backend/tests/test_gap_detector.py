from backend.ml.gap_detector import GapDetector, FeatureRow
from backend.ml.knowledge_tracing import BayesianKnowledgeTracer


def test_predict_mastery_range():
    detector = GapDetector()
    score = detector.predict_mastery([
        FeatureRow(accuracy_rate=0.8, avg_response_time=2200, attempt_count=8, error_pattern=0.2, concept_attempt_ratio=0.4),
        FeatureRow(accuracy_rate=0.4, avg_response_time=6000, attempt_count=7, error_pattern=0.7, concept_attempt_ratio=0.2),
    ])
    assert 0.0 <= score <= 1.0


def test_bkt_trace_monotonic_tendency():
    tracer = BayesianKnowledgeTracer()
    seq = tracer.trace_sequence([False, True, True, True])
    assert seq[-1] > seq[0]
