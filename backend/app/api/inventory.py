from typing import List, Union

from fastapi import APIRouter, Depends
from edgedb import AsyncIOConnection

from app.config import get_settings, Settings
from app.db import get_acon
from app.core.inventory.tasks import update_inventory
from app.crud import inventory
from app.models.pydantic.inventory import NetworkBasic, DesktopBasic

router = APIRouter()


@router.get("/update")
async def start_update_task(inventory: str, con: AsyncIOConnection = Depends(get_acon)):
    await update_inventory(con, inventory)
    return {"message": f"Starting {inventory} inventory update"}


@router.get("/network", response_model=List[NetworkBasic])
async def get_network_devices(
    con: AsyncIOConnection = Depends(get_acon),
    site: str = None,
    ip: str = None,
    hostname: str = None,
    platform: str = None,
    device_type: str = None,
    active: bool = True,
    shape: str = "basic",
):
    filter_criteria = []
    if site:
        filter_criteria.append({"site": site.split(",")})
    if ip:
        filter_criteria.append({"ip": ip.split(",")})
    if hostname:
        filter_criteria.append({"hostname": hostname.split(",")})
    if platform:
        filter_criteria.append({"platform": platform.split(",")})
    if device_type:
        filter_criteria.append({"device_type": device_type.split(",")})
    filter_criteria.append({"active": active})

    devices = await inventory.am_get(con, node_type="NetworkDevice", filter_criteria=filter_criteria, shape=shape)
    return devices


@router.get("/desktop", response_model=List[DesktopBasic])
async def get_network_devices(
    con: AsyncIOConnection = Depends(get_acon),
    site: str = None,
    ip: str = None,
    hostname: str = None,
    shape: str = "basic",
):
    filter_criteria = []
    if site:
        filter_criteria.append({"site": site.split(",")})
    if ip:
        filter_criteria.append({"ip": ip.split(",")})
    if hostname:
        filter_criteria.append({"hostname": hostname.split(",")})

    devices = await inventory.am_get(con, node_type="Desktop", filter_criteria=filter_criteria, shape=shape)
    return devices


@router.get("/search")
async def search_network_devices(
    q: str,
    con: AsyncIOConnection = Depends(get_acon),
):
    devices = await inventory.asearch(con, search_string=q)
    return devices
