# API Surface

## Gateway Prefix Mapping
- `/auth/*` -> Auth Service
- `/quiz/*` -> Quiz Engine
- `/performance/*` -> Student Performance
- `/recommendations/*` -> Recommendation Engine
- `/knowledge-graph/*` -> Knowledge Graph
- `/tutor/*` -> AI Tutor
- `/analytics/*` -> Analytics

## Core Endpoints
- `POST /auth/register`
- `POST /auth/login`
- `POST /quiz/submit`
- `GET /performance/mastery/{student_id}`
- `POST /recommendations/generate/{student_id}`
- `GET /knowledge-graph/prerequisites/{concept}`
- `POST /knowledge-graph/root-causes`
- `POST /tutor/chat`
- `GET /analytics/dashboard/{student_id}`
