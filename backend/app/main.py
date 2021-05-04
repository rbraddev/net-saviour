import logging

import uvicorn
from fastapi import FastAPI
import edgedb

from app.config import get_settings, Settings
from app.api import auth, ping

log = logging.getLogger(__name__)
db_pool: edgedb.AsyncIOPool
settings: Settings = get_settings()

def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(ping.router)
    application.include_router(auth.router, prefix="/auth", tags=["auth"])

    return application


app = create_application()


@app.on_event("startup")
async def startup() -> None:
    log.info("Starting up...")
    global db_pool
    db_pool = await edgedb.create_async_pool(
        host=settings.EDGEDB_HOST,
        database=settings.EDGEDB_DB,
        user=settings.EDGEDB_USER,
        password=settings.EDGEDB_PASSWORD,
    )
    log.info("Connected to EdgeDB")


@app.on_event("shutdown")
async def shutdown() -> None:
    log.info("Shutting down...")
    await db_pool.aclose()
    log.info("Closed connection to DB")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
