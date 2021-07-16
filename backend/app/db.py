import logging
from typing import AsyncGenerator

from edgedb import AsyncIOConnection, AsyncIOPool, create_async_pool, BlockingIOConnection, connect

from app.config import get_settings, Settings

log = logging.getLogger("uvicorn")
settings: Settings = get_settings()
db_pool: AsyncIOPool


async def create_db_pool() -> None:
    global db_pool
    log.info("Creating DB pool...")
    db_pool = await create_async_pool(
        host=settings.EDGEDB_HOST,
        database=settings.EDGEDB_DB,
        user=settings.EDGEDB_USER,
        password=settings.EDGEDB_PASSWORD,
    )


async def close_db_pool() -> None:
    await db_pool.aclose()


async def get_db_acon() -> AsyncGenerator[AsyncIOConnection, None]:
    try:
        con = await db_pool.acquire()
        yield con
    finally:
        await db_pool.release(con)


def get_con() -> BlockingIOConnection:
    con = connect(
        host=settings.EDGEDB_HOST,
        database=settings.EDGEDB_DB,
        user=settings.EDGEDB_USER,
        password=settings.EDGEDB_PASSWORD,
    )
    return con
