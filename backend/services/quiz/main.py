from fastapi import FastAPI
from backend.shared.contracts import QuizSubmission
from backend.shared.redis_client import redis_client

app = FastAPI(title="Quiz Engine")


@app.post("/submit")
async def submit_quiz(payload: QuizSubmission):
    await redis_client.xadd("quiz_submissions", {"payload": payload.model_dump_json()})
    await redis_client.set(f"last_quiz:{payload.student_id}", payload.model_dump_json(), ex=86400)
    return {"status": "queued", "answers": len(payload.answers), "student_id": payload.student_id}


@app.get("/health")
async def health():
    return {"status": "ok"}
