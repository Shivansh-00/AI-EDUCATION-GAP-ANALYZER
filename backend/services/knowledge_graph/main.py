from fastapi import FastAPI
from backend.shared.contracts import RootCauseRequest, RootCauseResponse

app = FastAPI(title="Knowledge Graph Service")

GRAPH = {
    "Calculus": ["Functions", "Algebra"],
    "Functions": ["Algebra", "Arithmetic"],
    "Probability": ["Algebra", "Arithmetic"],
    "Linear Algebra": ["Algebra"],
    "Trigonometry": ["Algebra", "Functions"],
}


@app.get("/prerequisites/{concept}")
async def prerequisites(concept: str):
    return {"concept": concept, "prerequisites": GRAPH.get(concept, [])}


@app.post("/root-causes", response_model=RootCauseResponse)
async def root_causes(payload: RootCauseRequest):
    prereqs = GRAPH.get(payload.target_concept, [])
    weak = [p for p in prereqs if payload.mastery.get(p, 1.0) < 0.6]
    return RootCauseResponse(target=payload.target_concept, root_causes=weak)
