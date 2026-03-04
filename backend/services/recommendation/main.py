from fastapi import FastAPI
from backend.shared.contracts import LearningPath, LearningPathStep, RecommendationRequest
from backend.shared.redis_client import redis_client

app = FastAPI(title="Recommendation Engine")


@app.post("/generate", response_model=LearningPath)
async def generate_path(payload: RecommendationRequest):
    steps = [
        LearningPathStep(
            concept=concept,
            reason=f"Prerequisite reinforcement for {payload.target_concept}",
            estimated_minutes=35,
        )
        for concept in payload.root_causes
    ]

    if payload.target_concept not in payload.root_causes:
        steps.append(
            LearningPathStep(
                concept=payload.target_concept,
                reason="Return to target concept after gap closure",
                estimated_minutes=45,
            )
        )

    path = LearningPath(student_id=payload.student_id, steps=steps)
    await redis_client.set(f"learning_path:{payload.student_id}", path.model_dump_json(), ex=86400)
    return path


@app.get("/path/{student_id}")
async def get_path(student_id: str):
    raw = await redis_client.get(f"learning_path:{student_id}")
    return {"data": raw}
