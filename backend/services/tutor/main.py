import httpx
from fastapi import FastAPI
from backend.shared.contracts import TutorQuery, TutorResponse
from backend.shared.config import settings

app = FastAPI(title="AI Tutor Service")

CONCEPT_SNIPPETS = {
    "Algebra": "Algebra is the language of symbols. Focus on balancing equations and manipulating expressions.",
    "Functions": "A function maps each input to exactly one output. Practice domain/range and transformations.",
    "Calculus": "Calculus studies change. Derivatives measure instantaneous rate of change.",
}


@app.post("/chat", response_model=TutorResponse)
async def chat(query: TutorQuery):
    async with httpx.AsyncClient(timeout=8) as client:
        mastery_resp = await client.get(f"{settings.performance_service_url}/mastery/{query.student_id}")

    mastery_data = mastery_resp.json().get("data") if mastery_resp.status_code == 200 else None
    weak = (mastery_data or {}).get("root_causes", [])[:2]

    contexts = [CONCEPT_SNIPPETS.get(c, "") for c in (query.concept_context + weak)]
    context_text = " ".join(c for c in contexts if c)
    answer = (
        f"Tutor guidance based on your current profile: {context_text}. "
        f"Weak foundations detected in: {', '.join(weak) if weak else 'none major'}.")
    answer += f"\n\nQuestion: {query.message}"

    follow_up_quiz = [
        {"question": "Solve: 2x + 3 = 11", "answer": "x = 4"},
        {"question": "What is derivative of x^2?", "answer": "2x"},
    ]
    return TutorResponse(answer=answer, follow_up_quiz=follow_up_quiz)
