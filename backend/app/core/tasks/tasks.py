from itertools import count
from os import confstr_names
from typing import *
import logging

from edgedb import AsyncIOConnection
from net_gsd import Runner

from app.runner import get_runner
from app.core.tasks.tracker import TaskTracker
from app.crud import inventory as inv
from app.core.runner.tasks import get_router_interface_detail, get_switch_interface_detail
from app.models.pydantic.inventory import Interface

log = logging.getLogger("uvicorn")


async def update_interface_details(con: AsyncIOConnection, tracker: TaskTracker, site: str = None, host: int = None):
    filter_criteria = [{"active": True}]
    if site:
        filter_criteria.append({"site": site.split(",")})
    elif host:
        filter_criteria.append({"nodeid": [int(i) for i in host.split(",")]})

    hosts = await inv.am_get(con, node_type="NetworkDevice", filter_criteria=filter_criteria, shape="basic")
    await tracker.set_total(str(len(hosts)))

    await update_switch_interface_details(con, [host for host in hosts if host["device_type"] == "switch"], tracker)
    await update_router_interface_details(con, [host for host in hosts if host["device_type"] == "router"], tracker)

    await tracker.set_status("complete")


async def update_switch_interface_details(con: AsyncIOConnection, hosts: list, tracker: TaskTracker):
    if hosts:
        runner: Runner = get_runner()
        results, failed = await runner.run_task(
            name="get switch interfaces", task=get_switch_interface_detail, hosts=hosts, tracker=tracker
        )
        await update_interface_details_db(con, results)


async def update_router_interface_details(con: AsyncIOConnection, hosts: list, tracker: TaskTracker):
    if hosts:
        runner: Runner = get_runner()
        results, failed = await runner.run_task(
            name="get router interfaces", task=get_router_interface_detail, hosts=hosts, tracker=tracker
        )
        # ADD LOGGING FOR NO HOSTS
        await update_interface_details_db(con, results)


async def update_interface_details_db(con: AsyncIOConnection, data: list):
    for host, interfaces in data.items():
        interfacelist = [
            Interface(
                name=interface,
                description=values.get("description") if values.get("description") else "",
                mac=values.get("mac"),
                ip=values.get("ip"),
                cidr=int(values.get("cidr")) if values.get("cidr") else 0,
                vlan=int(values.get("vlan")) if values.get("vlan") else 0,
                desktop=values.get("desktop") if values.get("desktop") else "NODEVICE",
            ).dict()
            for interface, values in interfaces.items()
        ]

        await inv.update_interfaces(con, hostname=host, interfacelist=interfacelist)
