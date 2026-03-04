import asyncio
import json
import httpx
from backend.shared.redis_client import redis_client
from backend.ml.gap_detector import GapDetector, FeatureRow
from backend.ml.features import build_features
from backend.shared.config import settings
from backend.shared.logger import get_logger
from backend.shared.monitoring import ML_INFERENCE_LATENCY, track_user_activity


log = get_logger("pipeline_worker")
detector = GapDetector()


async def process_submission(payload: dict):
    student_id = payload["student_id"]
    answers = payload["answers"]
    track_user_activity("quiz_submitted")

    grouped = {}
    for a in answers:
        grouped.setdefault(a["concept"], []).append(a)

    mastery = {}
    for concept, rows in grouped.items():
        f = build_features(rows)
        with ML_INFERENCE_LATENCY.labels(model="gap_detector").time():
            mastery[concept] = detector.predict_mastery([
                FeatureRow(
                    accuracy_rate=f["accuracy_rate"],
                    avg_response_time=f["avg_response_time"],
                    attempt_count=f["attempt_count"],
                    error_pattern=f["error_pattern"],
                    concept_attempt_ratio=f["concept_attempt_ratio"],
                )
            ])

    async with httpx.AsyncClient() as client:
        rc = await client.post(
            f"{settings.knowledge_graph_service_url}/root-causes",
            json={"mastery": mastery, "target_concept": "Calculus"},
        )
        root_causes = rc.json().get("root_causes", [])

        await client.post(
            f"{settings.performance_service_url}/mastery",
            json={
                "student_id": student_id,
                "mastery": [{"concept": k, "score": v} for k, v in mastery.items()],
                "root_causes": root_causes,
            },
        )

        await client.post(
            f"{settings.recommendation_service_url}/generate",
            json={
                "student_id": student_id,
                "target_concept": "Calculus",
                "root_causes": root_causes,
                "mastery": mastery,
            },
        )

    log.info(f"processed submission for {student_id}, root causes={root_causes}")


async def run_worker():
    stream = "quiz_submissions"
    group = "gap-workers"
    consumer = "worker-1"

    try:
        await redis_client.xgroup_create(stream, group, id="$", mkstream=True)
    except Exception:
        pass

    while True:
        events = await redis_client.xreadgroup(group, consumer, {stream: ">"}, count=5, block=5000)
        for _, entries in events:
            for event_id, fields in entries:
                payload = json.loads(fields["payload"])
                await process_submission(payload)
                await redis_client.xack(stream, group, event_id)


if __name__ == "__main__":
    asyncio.run(run_worker())
