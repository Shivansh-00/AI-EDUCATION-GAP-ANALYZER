# Deployment Guide

## Containerization
- Build per-service FastAPI containers from `backend/Dockerfile`.
- Build Next.js app from `frontend/Dockerfile`.

## Kubernetes
- Apply manifests in `infra/k8s`.
- Enable HPA using CPU + latency custom metrics.

## CI/CD
- GitHub Actions workflow runs lint/tests/build.
- On main branch, publish Docker images and deploy with rolling updates.

## Cloud Notes
- AWS: EKS + RDS + ElastiCache + Neo4j Aura.
- GCP: GKE + Cloud SQL + Memorystore.
- Azure: AKS + Azure Database for PostgreSQL + Azure Cache for Redis.
