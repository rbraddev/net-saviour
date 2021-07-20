from typing import *
from ipaddress import IPv4Address

from pydantic import BaseModel


class FailedHost(BaseModel):
    hostname: str
    ip: IPv4Address
    task: str
    error: str


class TaskStats(BaseModel):
    task_id: str
    name: str
    status: str
    total: int
    complete: int
    failed_count: int
    failed: List[FailedHost]
