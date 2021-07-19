import re
from typing import *
from uuid import uuid4
import logging

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from aioredis import RedisConnection
from edgedb import AsyncIOConnection

from app.core.tasks.tracker import TaskTracker, create_tracker
from app.core.tasks.tasks import update_interface_details
from app.db import get_db_acon
from app.redis import get_redis_con
import app.crud.inventory as inv

log = logging.getLogger("uvicorn")

router = APIRouter()


@router.get("/update_interfaces", status_code=201)
async def start_update_interface_task(
    background_tasks: BackgroundTasks,
    site: str = None,
    nodeid: str = None,
    db_con: AsyncIOConnection = Depends(get_db_acon),
    redis_con: RedisConnection = Depends(get_redis_con),
):
    """Update the interface details of all active nodes"""
    if site and nodeid:
        raise HTTPException(status_code=400, detail="Cannot filter by site and nodeid")
    tracker: TaskTracker = await create_tracker(redis_con, name="update interface details")
    background_tasks.add_task(update_interface_details, con=db_con, site=site, host=nodeid, tracker=tracker)
    return {"message": f"Starting interface update task", "task_id": tracker.task_id}


@router.get("/get_task")
async def get_task(task_id: str, con: RedisConnection = Depends(get_redis_con)):
    task = await create_tracker(con, task_id=task_id)
    result = await task.getall()
    return {"task": result}
