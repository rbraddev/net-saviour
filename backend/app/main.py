import uvicorn
from fastapi import FastAPI
import edgedb

from app.config import get_settings, Settings
from app.api import auth, ping, inventory, tasks
from app.db import create_db_pool, close_db_pool
from app.redis import create_redis_pool, close_redis_pool

db_pool: edgedb.AsyncIOPool
settings: Settings = get_settings()


def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT,
        on_startup=[create_db_pool, create_redis_pool],
        on_shutdown=[close_db_pool, close_redis_pool],
    )
    application.include_router(ping.router)
    application.include_router(auth.router, prefix="/auth", tags=["auth"])
    application.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
    application.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

    return application


app = create_application()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
