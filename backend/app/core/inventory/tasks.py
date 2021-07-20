import re
import logging

from edgedb import AsyncIOConnection
from deepdiff import DeepDiff
from net_gsd import Runner

from app.models.pydantic.inventory import Interface
from app.crud import inventory as inv
from app.core.inventory.utils import pull_network_inventory, pull_desktop_inventory, get_site

log = logging.getLogger("uvicorn")

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

    db_inventory: list = await inv.am_get(con, node_type=inventory["node_type"], shape="import")

    diff = DeepDiff(db_inventory, sw_inventory, view="tree", ignore_order=True)

    if diff:
        if "iterable_item_added" in diff.keys():
            await item_added(con, inventory, diff["iterable_item_added"])

        devices_to_update: dict = dict()
        if "values_changed" in diff.keys():
            values_changed(db_inventory, devices_to_update, diff["values_changed"])

        if "type_changes" in diff.keys():
            type_changes(db_inventory, devices_to_update, diff["type_changes"])

        for _, device in devices_to_update.items():
            await inv.aupdate(con, node_type=inventory["node_type"], data=device)
            log.info(f"updated {device['nodeid']}")

        if "iterable_item_removed" in diff.keys():
            await item_removed(con, inventory, diff["iterable_item_removed"])

    else:
        print("Inventory already up to date")


async def item_added(con: AsyncIOConnection, inventory: dict, diff: dict):
    for item in diff:
        device: dict = item.t2
        print(f"adding {device['nodeid']}")
        device.update({"site": get_site(device["hostname"])})
        result = await inv.acreate(con, node_type=inventory["node_type"], data=device)
        if result:
            log.info(f"added {device['nodeid']}")
        else:
            log.error(f"Error adding node {device['nodeid']}")


def values_changed(db_inventory: list, devices_to_update: dict, diff: dict):
    for item in diff:
        rx = re.match("^\D+(\d+)\W+(\w+).*$", item.path())
        # rx = re.match("^\D+(\d+)\D(\W+(\w+).*)*$", item.path())
        device = db_inventory[int(rx[1])]
        device.update({rx[2]: item.t2})
        devices_to_update.update({int(rx[1]): device})


def type_changes(db_inventory: list, devices_to_update: dict, diff: dict):
    for item in diff:
        rx = re.match("^\D+(\d+)\W+(\w+).*$", item.path())
        device = db_inventory[int(rx[1])]
        device.update({rx[2]: item.t2})
        devices_to_update.update({int(rx[1]): device})


async def item_removed(con: AsyncIOConnection, inventory: dict, diff: dict):
    for item in diff:
        device = item.t1
        await inv.aupdate(con, node_type=inventory["node_type"], data={"nodeid": device["nodeid"], "active": False})
        log.info(f"Deactivated {device['nodeid']}")
