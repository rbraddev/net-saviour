import logging

import uvicorn
from fastapi import FastAPI
import edgedb

from app.config import get_settings, Settings
from app.api import auth, ping
from app.db import create_pool, close_pool

log = logging.getLogger(__name__)
db_pool: edgedb.AsyncIOPool
settings: Settings = get_settings()


def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT,
        on_startup=[create_pool],
        on_shutdown=[close_pool],
    )
    application.include_router(ping.router)
    application.include_router(auth.router, prefix="/auth", tags=["auth"])

    return application


app = create_application()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
