from datetime import datetime
from typing import List, Dict
from pydantic import BaseModel, Field


class QuizAnswer(BaseModel):
    concept: str
    question_id: str
    selected: str
    correct: bool
    response_time_ms: int = Field(ge=0)


class QuizSubmission(BaseModel):
    student_id: str
    quiz_id: str
    answers: List[QuizAnswer]
    submitted_at: datetime = Field(default_factory=datetime.utcnow)


class MasteryScore(BaseModel):
    concept: str
    score: float = Field(ge=0.0, le=1.0)


class GapDiagnosis(BaseModel):
    student_id: str
    mastery: List[MasteryScore]
    root_causes: List[str]


class RootCauseRequest(BaseModel):
    mastery: Dict[str, float]
    target_concept: str


class RootCauseResponse(BaseModel):
    target: str
    root_causes: List[str]


class LearningPathStep(BaseModel):
    concept: str
    reason: str
    estimated_minutes: int


class LearningPath(BaseModel):
    student_id: str
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    steps: List[LearningPathStep]


class RecommendationRequest(BaseModel):
    student_id: str
    target_concept: str
    root_causes: List[str]
    mastery: Dict[str, float] = {}


class TutorQuery(BaseModel):
    student_id: str
    message: str
    concept_context: List[str] = []


class TutorResponse(BaseModel):
    answer: str
    follow_up_quiz: List[Dict[str, str]]
