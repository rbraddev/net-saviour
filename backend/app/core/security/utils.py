from datetime import datetime, timedelta
import importlib
from typing import Type

import jwt

from app.core.security.auth.base import Auth
import app.core.errors as errors
from app.config import get_settings


settings = get_settings()


def get_auth_mode() -> Type[Auth]:
    try:
        auth_mode = importlib.import_module(f"app.core.security.auth.{settings.AUTH_MODE.lower()}")
        auth_cls = getattr(auth_mode, f"{settings.AUTH_MODE.lower().capitalize()}Auth")
    except ModuleNotFoundError:
        raise errors.server_error("Unable to load authentication module")
    return auth_cls


def create_access_token(data: dict, expiry: int, key: str, algorithm: str) -> bytes:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expiry)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key, algorithm=algorithm)
    return encoded_jwt
