from fastapi import APIRouter, status

from app.application.entrypoints.schema.introspections.health import HealthCheck

introspections_router = APIRouter(prefix="/introspections", tags=["introspections"])


@introspections_router.get(
    "/health",
    responses={
        status.HTTP_200_OK: {"description": "Service is healthy."},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"description": "Service is unhealthy."},
    },
)
async def check_health() -> HealthCheck:
    return HealthCheck(status="healthy")
