from typing import List, Union

from fastapi import APIRouter, Depends
from edgedb import AsyncIOConnection

from app.config import get_settings, Settings
from app.db import get_acon
from app.crud import inventory
from app.models.pydantic.inventory import Network, Desktop

router = APIRouter()


@router.get("/network", response_model=List[Network])
async def get_network_devices(
    con: AsyncIOConnection = Depends(get_acon),
    site: str = None,
    ip: str = None,
    hostname: str = None,
    fields: str = None
):
    filter_criteria = []
    if site: filter_criteria.append({'site': site.split(',')})
    if ip: filter_criteria.append({'ip': ip.split(',')})
    if hostname: filter_criteria.append({'hostname': hostname.split(',')})
    if fields: fields = fields.split(',')

    devices = await inventory.am_get(con, node_type="NetworkDevice", filter_criteria=filter_criteria, fields=fields)
    return devices


@router.get("/search", response_model=List[Union[Network, Desktop]])
async def search_network_devices(
    search_string: str,
    con: AsyncIOConnection = Depends(get_acon),
):
    devices = await inventory.asearch(con, search_string=search_string)
    return devices