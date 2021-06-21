from typing import List, Dict
from ipaddress import IPv4Address

from pydantic import BaseModel


class Device(BaseModel):
    hostname: str
    ip: IPv4Address
    nodeid: int


class Desktop(Device):
    mac: str
    switch: List[Dict[str, str]]
    interface: List[Dict[str, str]]


class NetworkExtended(Device):
    interfaces: List[Dict[str, str]]
