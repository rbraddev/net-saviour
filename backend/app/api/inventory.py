from fastapi import APIRouter, Depends
from edgedb import AsyncIOConnection

from app.config import get_settings, Settings
from app.db import get_acon
from app.crud import inventory

router = APIRouter()


@router.get("/network")
async def get_network_devices(settings: Settings = Depends(get_settings), con: AsyncIOConnection = Depends(get_acon)):
    devices = await inventory.am_get(con, node_type="NetworkDevice")
    return devices
