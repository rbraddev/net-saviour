import json
from collections import namedtuple

from edgedb import BlockingIOConnection

from app import db
from app.crud import inventory
from app.core.inventory.utils import pull_sw_inventory


def update_inventory() -> None:
    sw_inventory = pull_sw_inventory()

    con: BlockingIOConnection = db.get_con()
    db_inventory = json.loads(inventory.m_get(con, node_type="NetworkDevice", fields=["nodeid", "ip", "hostname"]))

    if sw_inventory:
        Device = namedtuple("Device", "nodeid ip hostname")
        sw_ids = {Device(i["nodeid"], i["ipaddress"], i["nodename"]) for i in sw_inventory}
        db_ids = {Device(i["nodeid"], i["ip"], i["hostname"]) for i in db_inventory} if db_inventory else {}

        for device in sw_ids.difference(db_ids):
            if inventory.get(con, node_type="NetworkDevice", filter_criteria=[{"nodeid": device.nodeid}]):
                # update
                pass
            else:
                # insert
                pass

        for node in sw_inventory:
            con.query(
                """
                INSERT inventory::NetworkDevice {
                    nodeid := <int64>$NodeID,
                    hostname := <str>$NodeName,
                    ip := <str>$IPAddress,
                    image := <str>$IOSImage,
                }
            """,
                **node,
            )
