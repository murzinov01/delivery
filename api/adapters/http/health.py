"""Health check api."""

import fastapi
from fastapi import status


ROUTER: fastapi.APIRouter = fastapi.APIRouter()


@ROUTER.get("/liveness", status_code=status.HTTP_204_NO_CONTENT)
async def ping_service() -> None:
    """ASGI health check."""
    return
