# Architecture Notes

## Layers
1. Frontend (Next.js): React Query caching, mastery heatmap, knowledge graph visualization, learning timeline, Learning GPS, gamification widgets.
2. API Gateway (FastAPI): JWT validation + route proxy + centralized policy + Prometheus metrics.
3. Backend Services (FastAPI microservices): domain-segregated business logic.
4. ML Layer: feature engineering, model training pipeline (XGBoost/LightGBM), registry/versioning, inference, Bayesian Knowledge Tracing.
5. Data Layer: PostgreSQL + Neo4j + Redis.

## Asynchronous Pipeline
- Quiz submissions are appended to Redis Stream `quiz_submissions`.
- Worker consumes submissions and extracts engineered features.
- Mastery inference is executed and timed for observability.
- Root-cause concepts identified through knowledge-graph prerequisites.
- Recommendations generated and persisted/cached for dashboard retrieval.

## Demo Data
- `backend/scripts/generate_students.py` produces 500-1000 synthetic learners with quiz attempts and concept mastery snapshots for demos.
