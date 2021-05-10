from edgedb import BlockingIOConnection

from app import db
from app.core.inventory.utils import pull_sw_inventory


def update_inventory() -> None:
    sw_inventory = pull_sw_inventory()


    if sw_inventory:
        con: BlockingIOConnection = db.get_con()

        for node in sw_inventory:
            con.query("""
                INSERT inventory::NetworkDevice {
                    nodeid := <int64>$NodeID,
                    hostname := <str>$NodeName,
                    ip := <str>$IPAddress,
                    image := <str>$IOSImage,
                }
            """, **node)
