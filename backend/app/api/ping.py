from fastapi import APIRouter, Depends, Security

from app.config import get_settings, Settings
from app.core.security.utils import get_current_user
from app.models.pong import Pong, ProtectedPong

router = APIRouter()


@router.get("/ping", response_model=Pong)
async def pong(settings: Settings = Depends(get_settings)):
    return {
        "ping": "pong",
        "project": settings.PROJECT,
        "environment": settings.ENVIRONMENT,
    }


@router.get("/protected_ping", response_model=ProtectedPong)
async def protected_pong(
    username: str = Security(get_current_user),
    settings: Settings = Depends(get_settings),
):
    return {
        "ping": "pong",
        "project": settings.PROJECT,
        "environment": settings.ENVIRONMENT,
        "username": username,
    }
