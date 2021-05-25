from uuid import UUID
from ipaddress import IPv4Address

from pydantic import BaseModel


class Device(BaseModel):
    id: UUID
    hostname: str
    ip: IPv4Address


class Network(Device):
    nodeid: int


class Desktop(Device):
    mac: str