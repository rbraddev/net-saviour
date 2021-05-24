import json
from collections import namedtuple

from celery import Celery
from edgedb import BlockingIOConnection

from app import db
from app.crud import inventory
from app.core.inventory.utils import pull_sw_inventory, get_site


def update_inventory() -> None:
    sw_inventory = pull_sw_inventory()

    con: BlockingIOConnection = db.get_con()
    db_inventory = json.loads(inventory.m_get(con, node_type="NetworkDevice", fields=["nodeid", "ip", "hostname"]))

    if sw_inventory:
        Device = namedtuple("Device", "nodeid ip hostname")
        sw_ids = {Device(i["nodeid"], i["ipaddress"], i["nodename"]) for i in sw_inventory}
        db_ids = {Device(i["nodeid"], i["ip"], i["hostname"]) for i in db_inventory} if db_inventory else set()

        if sw_ids.difference(db_ids) or db_ids.difference(sw_ids):
            for device in sw_ids.difference(db_ids):
                if inventory.get(con, node_type="NetworkDevice", filter_criteria=[{"nodeid": device.nodeid}]):
                    print(f"updating {device.nodeid}")
                    inventory.update(con, node_type="NetworkDevice", data=device._asdict())
                    print(f"updated {device.nodeid}")
                else:
                    print(f"adding {device.nodeid}")
                    device_data = device._asdict()
                    device_data.update({"site": get_site(device.hostname)})
                    inventory.create(con, node_type="NetworkDevice", data=device_data)
                    print(f"added {device.nodeid}")

            for device in db_ids.difference(sw_ids):
                print(f"Deactivating {device.nodeid}")
                inventory.update(con, node_type="NetworkDevice", data={"nodeid": device.nodeid, "active": False})
        else:
            print("Inventory already up tp date")
