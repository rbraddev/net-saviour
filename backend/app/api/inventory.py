from typing import *

from fastapi import APIRouter, Depends, HTTPException
from edgedb import AsyncIOConnection

from app.db import get_acon
from app.core.inventory.tasks import update_inventory, update_interface_details
from app.crud import inventory
from app.models.pydantic.inventory import NetworkBasic, DesktopBasic, NetworkExtended, Search

router = APIRouter()


@router.get("/update", status_code=201)
async def start_update_task(inventory: str, con: AsyncIOConnection = Depends(get_acon)):
    """Update the SOT inventory of network devices and desktops"""
    await update_inventory(con, inventory.lower())
    return {"message": f"Starting {inventory} inventory update task"}

@router.get("/update_interfaces", status_code=201)
async def start_update_interface_task(site: str = None, nodeid: int = None, con: AsyncIOConnection = Depends(get_acon)):
    """Update the interface details of all active nodes"""
    if site and nodeid:
        raise HTTPException(status_code=400, detail="Cannot filter by site and nodeid")
    await update_interface_details(con, site=site, host=nodeid)
    return {"message": f"Starting interface update task"}

@router.get("/network", response_model=List[NetworkExtended], status_code=200)
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
    con: AsyncIOConnection = Depends(get_acon),
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
    con: AsyncIOConnection = Depends(get_acon),
):
    """search for network devices and desktops by partial or complete ip, mac or hostname"""
    devices = await inventory.asearch(con, search_string=q)
    return devices
