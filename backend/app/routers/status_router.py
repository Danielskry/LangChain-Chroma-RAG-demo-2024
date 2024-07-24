from typing import Dict, Any

from fastapi import APIRouter, Depends

from app.schemas.status_schema import Status

status_router = APIRouter()

@status_router.get("/status", response_model=Status, tags=["Status"])
async def get_status() -> Dict[str, str]:
    """
    Get system status.

    This endpoint is exposed and used as a health check to ensure the service is up and running.

    Returns:
    - Status: An object containing the status message.
    """
    return {"status": "OK", "message": "Service is up and running."}
