import logging

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.config import get_settings, Settings
from app.core.security.utils import get_auth_mode, create_access_token
from app.models.token import Token


router = APIRouter()
httpbasic = HTTPBasic()

log = logging.getLogger(__name__)


@router.post("/token", response_model=Token)
async def get_access_token(
    credentials: HTTPBasicCredentials = Depends(httpbasic),
    settings: Settings = Depends(get_settings),
):
    auth_mode = get_auth_mode(settings.AUTH_MODE)
    auth = auth_mode(credentials.username, credentials.password)

    await auth.aauthenticate() if auth_mode.concurrency == "async" else auth.authenticate()

    expiry, key, algorithm = (
        settings.AUTH_TOKEN_EXPIRY,
        settings.AUTH_KEY,
        settings.TOKEN_ALGORITHM,
    )
    access_token = create_access_token(
        data={"sub": credentials.username},
        expiry=expiry,
        key=key,
        algorithm=algorithm,
    )
    return {"access_token": access_token, "token_type": "bearer"}
