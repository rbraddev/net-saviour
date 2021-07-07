from typing import List, Dict
from ipaddress import IPv4Address

from pydantic import BaseModel


class Device(BaseModel):
    hostname: str
    ip: IPv4Address
    nodeid: int


class NetworkBasic(Device):
    device_type: str
    platform: str


class DesktopBasic(Device):
    cidr: int
    mac: str


class Desktop(Device):
    switch: List[Dict[str, str]]
    interface: List[Dict[str, str]]


class NetworkExtended(Device):
    interfaces: List[Dict[str, str]]
