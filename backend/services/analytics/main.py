import asyncio
import json
import httpx
from fastapi import FastAPI
from backend.shared.config import settings

app = FastAPI(title="Analytics Service")


@app.get("/dashboard/{student_id}")
async def dashboard(student_id: str):
    async with httpx.AsyncClient(timeout=10) as client:
        mastery_req = client.get(f"{settings.performance_service_url}/mastery/{student_id}")
        path_req = client.get(f"{settings.recommendation_service_url}/path/{student_id}")
        mastery_res, path_res = await asyncio.gather(mastery_req, path_req)

    mastery_data = mastery_res.json().get("data") if mastery_res.status_code == 200 else None
    path_data = path_res.json().get("data") if path_res.status_code == 200 else None

    if isinstance(path_data, str):
        path_data = json.loads(path_data)

    mastery_map = {m["concept"]: m["score"] for m in (mastery_data or {}).get("mastery", [])} if mastery_data else {}
    weak = sorted(mastery_map.items(), key=lambda x: x[1])[:3]

    return {
        "student_id": student_id,
        "mastery": mastery_map,
        "root_causes": (mastery_data or {}).get("root_causes", []),
        "weakest_concepts": weak,
        "learning_path": path_data,
        "weekly_accuracy": [0.56, 0.61, 0.64, 0.72],
        "time_on_task_minutes": 240,
    }
