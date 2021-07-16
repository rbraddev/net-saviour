from os import name
from typing import *
from ipaddress import IPv4Address, ip_address

from pydantic import BaseModel


class Device(BaseModel):
    hostname: str
    ip: IPv4Address
    nodeid: int
    site: str


class NetworkBasic(Device):
    device_type: str
    platform: str
    active: bool


class DesktopBasic(Device):
    cidr: int
    mac: str


class NetworkSearch(BaseModel):
    hostname: str
    ip: IPv4Address
    nodeid: int


class Desktop(Device):
    switch: List[NetworkSearch]
    interface: List[Dict[str, str]]


class Interface(BaseModel):
    name: str
    description: Optional[str]
    mac: Optional[str]
    ip: Optional[str]
    cidr: Optional[int]
    vlan: Optional[int]
    desktop: Union[Optional[DesktopBasic], str]


class NetworkExtended(Device):
    interfaces: List[Interface]


class InterfaceSearch(Interface):
    switch: List[Device]


class Search(BaseModel):
    network: Optional[List[Device]]
    desktop: Optional[List[Desktop]]
    interface: Optional[list[InterfaceSearch]]
