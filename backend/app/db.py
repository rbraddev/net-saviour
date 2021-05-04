from typing import AsyncGenerator

from edgedb import AsyncIOConnection, AsyncIOPool, create_async_pool

from app.config import settings

db_pool: AsyncIOPool


async def create_pool() -> None:
    global db_pool
    db_pool = await create_async_pool(
        host=settings.EDGEDB_HOST,
        database=settings.EDGEDB_DB,
        user=settings.EDGEDB_USER,
    )


async def close_pool() -> None:
    await db_pool.aclose()


async def get_con() -> AsyncGenerator[AsyncIOConnection, None]:
    try:
        con = await db_pool.acquire()
        yield con
    finally:
        await db_pool.release(con)
