import json
import re

from celery import Celery
from edgedb import BlockingIOConnection
from deepdiff import DeepDiff

from app import db
from app.crud import inventory as inv
from app.core.inventory.utils import pull_network_inventory, pull_desktop_inventory, get_site


inventory_dict = {
    "network": {
        "inventory": pull_network_inventory,
        "keys": ["nodeid", "ip", "hostname", "platform", "active"],
        "node_type": "NetworkDevice",
    },
    "desktop": {
        "inventory": pull_desktop_inventory,
        "keys": ["nodeid", "ip", "cidr", "mac", "hostname", "active"],
        "node_type": "Desktop",
    },
}


def update_inventory(inventory_type: str) -> None:
    if inventory_type not in ["network", "desktop"]:
        raise ValueError("Inventory must be of type 'network' or 'desktop'")

    inventory: dict = inventory_dict.get(inventory_type)

    sw_inventory: list = inventory["inventory"]()

    con: BlockingIOConnection = db.get_con()
    db_inventory: list = json.loads(inv.m_get(con, node_type=inventory["node_type"], shape="basic"))

    diff = DeepDiff(db_inventory, sw_inventory, view="tree", ignore_order=True)
    print(diff)

    if diff:
        print(diff.keys())
        if "iterable_item_added" in diff.keys():
            for item in diff["iterable_item_added"]:
                device: dict = item.t2
                print(f"adding {device['nodeid']}")
                device.update({"site": get_site(device["hostname"])})
                result = inv.create(con, node_type=inventory["node_type"], data=device)
                if result:
                    print(f"added {device['nodeid']}")
                else:
                    print(f"Error adding node {device['nodeid']}")

        devices_to_update: dict = dict()
        if "values_changed"in diff.keys():
            for item in diff["values_changed"]:
                rx = re.match("^\D+(\d+)\W+(\w+).*$", item.path())
                device = db_inventory[int(rx[1])]
                device.update({rx[2]: item.t2})
                devices_to_update.update({int(rx[1]): device})
            
        if "type_changes"in diff.keys():
            for item in diff["type_changes"]:
                rx = re.match("^\D+(\d+)\W+(\w+).*$", item.path())
                device = db_inventory[int(rx[1])]
                device.update({rx[2]: item.t2})
                devices_to_update.update({int(rx[1]): device})
            
        for _, device in devices_to_update.items():
            print(device)
            print(f"updating {device['nodeid']}")
            inv.update(con, node_type=inventory["node_type"], data=device)
            print(f"updated {device['nodeid']}")

        if "iterable_item_removed" in diff.keys():
            for item in diff["iterable_item_removed"]:
                device = item.t1
                print(f"Deactivating {device['nodeid']}")
                inv.update(con, node_type=inventory["node_type"], data={"nodeid": device["nodeid"], "active": False})
                print(f"Deactivated {device['nodeid']}")

    else:
        print("Inventory already up to date")
