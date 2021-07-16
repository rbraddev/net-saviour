from typing import *

from fastapi import APIRouter, Depends, HTTPException
from edgedb import AsyncIOConnection

from app.db import get_db_acon
from app.redis import get_redis_con
from app.core.inventory.tasks import update_inventory
from app.crud import inventory
from app.models.pydantic.inventory import DesktopBasic, NetworkExtended, Search

router = APIRouter()


@router.get("/update", status_code=201)
async def start_update_task(inventory: str, con: AsyncIOConnection = Depends(get_db_acon)):
    """Update the SOT inventory of network devices and desktops"""
    try:
        await update_inventory(con, inventory.lower())
    except:
        raise HTTPException(status_code=500, detail="Error occured updating the inventory, please see logs")
    return {"message": f"{inventory} inventory update task completed"}


@router.get("/network", response_model=List[NetworkExtended], status_code=200)
async def get_network_devices(
    con: AsyncIOConnection = Depends(get_db_acon),
    site: str = None,
    ip: str = None,
    hostname: str = None,
    platform: str = None,
    device_type: str = None,
    active: bool = True,
    shape: str = "basic",
):
    """Search for network devices"""
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


@router.get("/desktop", response_model=List[DesktopBasic], status_code=200)
async def get_network_devices(
    con: AsyncIOConnection = Depends(get_db_acon),
    site: str = None,
    ip: str = None,
    hostname: str = None,
    shape: str = "basic",
):
    """Search for desktops"""
    filter_criteria = []
    if site:
        filter_criteria.append({"site": site.split(",")})
    if ip:
        filter_criteria.append({"ip": ip.split(",")})
    if hostname:
        filter_criteria.append({"hostname": hostname.split(",")})

    devices = await inventory.am_get(con, node_type="Desktop", filter_criteria=filter_criteria, shape=shape)
    return devices


@router.get("/search", response_model=Search, status_code=200)
async def search_network_devices(
    q: str,
    con: AsyncIOConnection = Depends(get_db_acon),
):
    """search for network devices and desktops by partial or complete ip, mac or hostname"""
    devices = await inventory.asearch(con, search_string=q)
    return devices
