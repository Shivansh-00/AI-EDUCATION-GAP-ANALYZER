import json
from fastapi import FastAPI
from backend.shared.contracts import GapDiagnosis
from backend.shared.redis_client import redis_client

app = FastAPI(title="Student Performance Service")


@app.post("/mastery")
async def store_mastery(diagnosis: GapDiagnosis):
    key = f"mastery:{diagnosis.student_id}"
    await redis_client.set(key, diagnosis.model_dump_json(), ex=86400)
    return {"status": "stored", "root_causes": diagnosis.root_causes}


@app.get("/mastery/{student_id}")
async def get_mastery(student_id: str):
    result = await redis_client.get(f"mastery:{student_id}")
    return {"data": json.loads(result) if result else None}
