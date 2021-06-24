import logging
import os
import secrets
from functools import lru_cache

from pydantic import BaseSettings
from kombu import Queue

log = logging.getLogger(__name__)


def route_task(name, args, kwargs, options, task=None, **kw):
    if ":" in name:
        queue, _ = name.split(":")
        return {"queue": queue}
    return {"queue": "default"}


class Settings(BaseSettings):
    PROJECT: str = os.getenv("PROJECT", "FastAPI")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "dev")
    AUTH_KEY: str = os.environ.get("AUTH_SECRET_KEY", secrets.token_urlsafe(32))
    AUTH_TOKEN_EXPIRY: int = os.environ.get("AUTH_TOKEN_EXPIRY", 30)
    TOKEN_ALGORITHM: str = os.environ.get("TOKEN_ALGORITHM", "HS256")
    AUTH_MODE: str = os.environ.get("AUTH_MODE")

    API_USER: str = os.environ.get("API_USER")
    API_PASSWORD: str = os.environ.get("API_PASSWORD")

    EDGEDB_HOST: str = os.environ.get("EDGEDB_HOST", "localhost")
    EDGEDB_USER: str = os.environ.get("EDGEDB_USER", "edgedb")
    EDGEDB_PASSWORD: str = os.environ.get("EDGEDB_PASSWORD", "edgedb")
    EDGEDB_DB: str = os.environ.get("EDGEDB_DB", "edgedb")

    TACACS_SVR: str = os.environ.get("TACACS_HOST", "localhost")
    TACACS_KEY: str = os.environ.get("TACACS_PLUS_KEY")

    SW_HOST: str = os.environ.get("SW_HOST")
    SW_USER: str = os.environ.get("SW_USER")
    SW_PASSWORD: str = os.environ.get("SW_PASSWORD")


class CeleryConfig:
    broker_url = os.environ.get("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
    result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0")
    task_default_queue = "default"
    task_create_missing_queues = False
    task_queues = (
        Queue("default"),
        Queue("high_priority"),
        Queue("low_priority"),
    )
    task_routes = (route_task,)


@lru_cache
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()
