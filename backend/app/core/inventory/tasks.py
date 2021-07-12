import re

from edgedb import AsyncIOConnection
from deepdiff import DeepDiff
from net_gsd import Runner

from app.runner import get_runner
from app.core.runner.tasks import get_switch_interface_detail, get_router_interface_detail
from app.models.pydantic.inventory import Interface
from app.crud import inventory as inv
from app.core.inventory.utils import pull_network_inventory, pull_desktop_inventory, get_site


inventory_dict = {
    "network": {
        "inventory": pull_network_inventory,
        "keys": ["nodeid", "ip", "hostname", "device_type", "platform", "active"],
        "node_type": "NetworkDevice",
    },
    "desktop": {
        "inventory": pull_desktop_inventory,
        "keys": ["nodeid", "ip", "cidr", "mac", "hostname", "active"],
        "node_type": "Desktop",
    },
}


async def update_inventory(con: AsyncIOConnection, inventory_type: str) -> None:
    """Pulls network and desktop inventory from Solarwinds"""
    if inventory_type not in ["network", "desktop"]:
        raise ValueError("Inventory must be of type 'network' or 'desktop'")

    inventory: dict = inventory_dict.get(inventory_type)

    sw_inventory: list = await inventory["inventory"]()

    db_inventory: list = await inv.am_get(con, node_type=inventory["node_type"], shape="basic")

    diff = DeepDiff(db_inventory, sw_inventory, view="tree", ignore_order=True)

    if diff:
        if "iterable_item_added" in diff.keys():
            for item in diff["iterable_item_added"]:
                device: dict = item.t2
                print(f"adding {device['nodeid']}")
                device.update({"site": get_site(device["hostname"])})
                result = await inv.acreate(con, node_type=inventory["node_type"], data=device)
                if result:
                    print(f"added {device['nodeid']}")
                else:
                    print(f"Error adding node {device['nodeid']}")

        devices_to_update: dict = dict()
        if "values_changed" in diff.keys():
            for item in diff["values_changed"]:
                rx = re.match("^\D+(\d+)\W+(\w+).*$", item.path())
                # rx = re.match("^\D+(\d+)\D(\W+(\w+).*)*$", item.path())
                device = db_inventory[int(rx[1])]
                device.update({rx[2]: item.t2})
                devices_to_update.update({int(rx[1]): device})

        if "type_changes" in diff.keys():
            for item in diff["type_changes"]:
                rx = re.match("^\D+(\d+)\W+(\w+).*$", item.path())
                device = db_inventory[int(rx[1])]
                device.update({rx[2]: item.t2})
                devices_to_update.update({int(rx[1]): device})

        for _, device in devices_to_update.items():
            print(device)
            print(f"updating {device['nodeid']}")
            await inv.aupdate(con, node_type=inventory["node_type"], data=device)
            print(f"updated {device['nodeid']}")

        if "iterable_item_removed" in diff.keys():
            for item in diff["iterable_item_removed"]:
                device = item.t1
                print(f"Deactivating {device['nodeid']}")
                await inv.aupdate(
                    con, node_type=inventory["node_type"], data={"nodeid": device["nodeid"], "active": False}
                )
                print(f"Deactivated {device['nodeid']}")

    else:
        print("Inventory already up to date")


async def update_interface_details(con: AsyncIOConnection, site: str = None, host: int = None):
    filter_criteria = [{"active": True}]
    if site:
        filter_criteria.append({"site": str(site)})
    elif host:
        filter_criteria.append({"nodeid": int(host)})

    await update_switch_interface_details(con, filter_criteria)
    await update_router_interface_details(con, filter_criteria)


async def update_switch_interface_details(con: AsyncIOConnection, filter_criteria: list):
    filter_criteria.append({"device_type": "switch"})
    hosts = await inv.am_get(con, node_type="NetworkDevice", filter_criteria=filter_criteria, shape="basic")
    if hosts:
        runner: Runner = get_runner()
        results, failed = await runner.run_task(
            name="get switch interfaces", task=get_switch_interface_detail, hosts=hosts
        )
        # ADD LOGGING FOR NO HOSTS
        await update_interface_details_db(con, results)


async def update_router_interface_details(con: AsyncIOConnection, filter_criteria: list):
    filter_criteria.append({"device_type": "router"})
    hosts = await inv.am_get(con, node_type="NetworkDevice", filter_criteria=filter_criteria, shape="basic")
    if hosts:
        runner: Runner = get_runner()
        results, failed = await runner.run_task(
            name="get router interfaces", task=get_router_interface_detail, hosts=hosts
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
