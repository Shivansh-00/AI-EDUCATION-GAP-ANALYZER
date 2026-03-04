# AI EDUCATION GAP ANALYZER

Production-grade, microservice-style AI platform for diagnosing hidden conceptual learning gaps and generating personalized mastery pathways.

## 1) High-Level Architecture Diagram

```mermaid
flowchart LR
    FE[Next.js Frontend\nDashboard, Heatmap, Graph, Timeline, GPS, Gamification] -->|JWT + HTTPS| GW[FastAPI API Gateway]
    GW --> AUTH[Auth Service]
    GW --> QUIZ[Quiz Engine Service]
    GW --> PERF[Performance Service]
    GW --> RECO[Recommendation Service]
    GW --> KG[Knowledge Graph Service]
    GW --> TUTOR[AI Tutor Service]
    GW --> AN[Analytics Service]

    QUIZ --> PG[(PostgreSQL)]
    PERF --> PG
    RECO --> PG
    AUTH --> PG
    AN --> PG

    KG --> NEO[(Neo4j)]

    QUIZ -->|events| REDIS[(Redis Streams/Cache)]
    REDIS --> WORKER[Background Worker]
    WORKER --> FEAT[Feature Engineering]
    FEAT --> ML[Gap Detection Models\n(RandomForest/XGBoost/LightGBM)]
    ML --> REG[Model Registry]
    ML --> BKT[Bayesian Knowledge Tracing]
    WORKER --> KG
    WORKER --> RECO

    GW --> MON[Prometheus Metrics]
```

## 2) Monorepo Structure
- `frontend/` — Next.js App Router app (TypeScript, Tailwind, Zustand, React Query, Recharts, React Flow).
- `backend/` — API Gateway + microservices + shared models + workers + ML modules + synthetic data scripts.
- `infra/` — Docker Compose, Kubernetes manifests, Terraform starter.
- `docs/` — schema, API contracts, event flows, scaling notes.

## 3) Quick Start
```bash
docker compose up --build
```

## 4) Core Upgrades Included
- Knowledge Graph visualization component (`KnowledgeGraph.tsx`) with mastery-color nodes.
- Learning Timeline analytics (`LearningTimeline.tsx`) for mastery-over-time.
- Learning GPS navigation widget (`LearningGPS.tsx`) as path-to-mastery UX.
- ML training pipeline (`train_model.py`) with XGBoost/LightGBM.
- Feature engineering module (`features.py`) and model versioning registry (`model_registry.py`).
- Demo data generator (`generate_students.py`) for 500-1000 student datasets.
- Logging + monitoring (`logger.py`, `monitoring.py`) and `/metrics` endpoint.
- Gamification components (`Leaderboard.tsx`, `Badges.tsx`).
- Bayesian Knowledge Tracing (`knowledge_tracing.py`) for evolving mastery estimation.
