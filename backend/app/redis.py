import logging
from typing import *

import aioredis
from aioredis import ConnectionsPool, RedisConnection

from app.config import Settings, get_settings

log = logging.getLogger("uvicorn")
settings: Settings = get_settings()
redis_pool: ConnectionsPool


async def create_redis_pool():
    global redis_pool
    log.info("Creating Redis pool...")
    redis_pool = await aioredis.create_pool(f"redis://{settings.REDIS_SERVER}")


async def close_redis_pool():
    await redis_pool.close()


async def get_redis_con() -> AsyncGenerator[RedisConnection, None]:
    try:
        con = await redis_pool.acquire()
        yield con
    finally:
        redis_pool.release(con)
