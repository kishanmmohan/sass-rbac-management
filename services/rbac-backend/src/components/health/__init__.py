from fastapi import APIRouter, Depends

from config import Settings, get_settings

router = APIRouter()


@router.get("/health")
async def health(settings: Settings = Depends(get_settings)):
    return {"status": "active", "environment": settings.environment, "testing": settings.testing}
