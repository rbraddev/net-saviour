from typing import *
import functools
from ast import literal_eval
from dataclasses import dataclass, field
from uuid import uuid4
from itertools import chain
import logging

from aioredis import RedisConnection

from app.core.tasks.errors import NoTaskName, NoTaskFound

log = logging.getLogger("uvicorn")


@dataclass
class TaskTracker:
    _con: RedisConnection = field(repr=False)
    task_id: str = field(default=None)
    name: str = field(default=None)

    async def _init(self):
        if not self.task_id:
            self.task_id = str(uuid4())
            if not self.name:
                raise NoTaskName("Task requires a name")
            task_defaults = {"name": self.name, "status": "pending", "total": 0, "complete": 0}
            await self._set(task_defaults)
        else:
            task_data: dict = await self.getall()
            if task_data:
                self.name = task_data.get("name")
            else:
                raise NoTaskFound("No tasks found with Task ID provided")

    async def completed(self):
        await self._con.execute("HINCRBY", self.task_id, "complete", "1")

    async def set_status(self, status: str):
        await self._set({"status": status})

    async def set_result(self, result: dict):
        await self._set({"result": str(result)})

    async def set_total(self, total: str):
        await self._set({"total": str(total)})

    async def _set(self, data: dict) -> None:
        await self._con.execute("HSET", self.task_id, *chain.from_iterable(data.items()))

    async def getall(self):
        task_data = await self._con.execute("HGETALL", self.task_id)
        if task_data:
            task_dict = {k: v for k, v in zip(*[iter(task_data)] * 2)}
            task_dict.update({"task_id": self.task_id})
            task_result = task_dict.get("result")
            if task_result:
                task_dict["result"] = literal_eval(task_result)
        return task_dict if task_dict else {}

    async def get(self, key: str) -> Union[str, dict]:
        value = await self._con.execute("HGET", self.task_id, key, encoding="utf-8")
        return literal_eval(value) if key == "result" else value


async def create_tracker(con: RedisConnection, task_id: str = None, name: str = None) -> TaskTracker:
    task = TaskTracker(con, task_id=task_id, name=name)
    await task._init()
    return task


def track(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        tracker: TaskTracker = kwargs["tracker"]
        result = await func(*args)
        await tracker.completed()
        return result

    return wrapper
