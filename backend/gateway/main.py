import time
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import httpx
from backend.shared.config import settings
from backend.shared.security import decode_access_token
from backend.shared.logger import get_logger
from backend.shared.monitoring import track_request, request_timer, metrics_router
from backend.shared.redis_client import redis_client

app = FastAPI(title="API Gateway", version="1.0.0")
app.include_router(metrics_router())
log = get_logger("gateway")

SERVICE_MAP = {
    "/auth": settings.auth_service_url,
    "/quiz": settings.quiz_service_url,
    "/performance": settings.performance_service_url,
    "/recommendations": settings.recommendation_service_url,
    "/knowledge-graph": settings.knowledge_graph_service_url,
    "/tutor": settings.tutor_service_url,
    "/analytics": settings.analytics_service_url,
}


async def _rate_limit(client_id: str, limit: int = 120, window_sec: int = 60) -> bool:
    window = int(time.time()) // window_sec
    key = f"ratelimit:{client_id}:{window}"
    count = await redis_client.incr(key)
    if count == 1:
        await redis_client.expire(key, window_sec)
    return count <= limit


@app.middleware("http")
async def auth_and_rate_limit(request: Request, call_next):
    if request.url.path == "/metrics":
        return await call_next(request)

    client_id = request.client.host if request.client else "unknown"
    if not await _rate_limit(client_id):
        return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})

    if not request.url.path.startswith("/auth"):
        auth_header = request.headers.get("authorization", "")
        if not auth_header.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Missing token"})
        token = auth_header.split(" ", 1)[1]
        try:
            decode_access_token(token)
        except Exception:
            return JSONResponse(status_code=401, content={"detail": "Invalid token"})
    return await call_next(request)


@app.api_route('/{full_path:path}', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
async def proxy(full_path: str, request: Request):
    path = f"/{full_path}"
    prefix = next((p for p in SERVICE_MAP if path.startswith(p)), None)
    if not prefix:
        raise HTTPException(status_code=404, detail="Unknown route")

    target = f"{SERVICE_MAP[prefix]}{path[len(prefix):]}"
    track_request("gateway", prefix, request.method)
    with request_timer("gateway", prefix):
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.request(
                method=request.method,
                url=target,
                headers={k: v for k, v in request.headers.items() if k.lower() != 'host'},
                params=request.query_params,
                content=await request.body(),
            )

    log.info(f"proxied {request.method} {path} -> {target} [{response.status_code}]")
    try:
        payload = response.json()
    except Exception:
        payload = {"raw": response.text}
    return JSONResponse(status_code=response.status_code, content=payload)
