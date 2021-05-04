import logging
import os
import secrets
from functools import lru_cache

from pydantic import BaseSettings

log = logging.getLogger(__name__)


class Settings(BaseSettings):
    PROJECT: str = os.getenv("PROJECT", "FastAPI")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "dev")
    AUTH_KEY: str = os.environ.get("AUTH_SECRET_KEY", secrets.token_urlsafe(32))
    AUTH_TOKEN_EXPIRY: int = os.environ.get("AUTH_TOKEN_EXPIRY", 30)
    TOKEN_ALGORITHM: str = os.environ.get("TOKEN_ALGORITHM", "HS256")
    AUTH_MODE: str = os.environ.get("AUTH_MODE")

    EDGEDB_HOST: str = os.environ.get("EDGEDB_HOST", "nsav-db")
    EDGEDB_USER: str = os.environ.get("EDGEDB_USER", "edgedb")
    EDGEDB_PASSWORD: str = os.environ.get("EDGEDB_PASSWORD", "edgedb")
    EDGEDB_DB: str = os.environ.get("EDGEDB_DB", "edgedb")

    TACACS_SVR: str = os.environ.get("TACACS_HOST", "localhost")
    TACACS_KEY: str = os.environ.get("TACACS_PLUS_KEY")


@lru_cache
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()
