import time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import APIRouter, Response

REQUEST_COUNT = Counter("edgap_requests_total", "Total API requests", ["service", "endpoint", "method"])
REQUEST_LATENCY = Histogram("edgap_request_latency_seconds", "Request latency", ["service", "endpoint"])
ML_INFERENCE_LATENCY = Histogram("edgap_ml_inference_latency_seconds", "ML inference latency", ["model"])
USER_ACTIVITY = Counter("edgap_user_activity_total", "User activity events", ["activity"])


def track_request(service: str, endpoint: str, method: str):
    REQUEST_COUNT.labels(service=service, endpoint=endpoint, method=method).inc()


def request_timer(service: str, endpoint: str):
    return REQUEST_LATENCY.labels(service=service, endpoint=endpoint).time()


def track_user_activity(activity: str):
    USER_ACTIVITY.labels(activity=activity).inc()


def metrics_router() -> APIRouter:
    router = APIRouter()

    @router.get("/metrics")
    async def metrics():
        return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

    return router
