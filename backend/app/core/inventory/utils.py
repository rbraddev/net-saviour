import re
from typing import Union, List, Dict, Any

from httpx import Response, Client

from app.config import Settings, get_settings

settings: Settings = get_settings()


def query_sw(query: str, parameters: dict) -> List[Dict[str, Any]]:
    headers = {"Content-Type": "application/json"}
    data = {
        "query": query,
        "parameters": parameters,
    }

    with Client() as client:
        response: Response = client.get(
            f"https://{{settings.SW_HOST}}:17778/SolarWinds/InformationService/v3/Json/Query",
            headers=headers,
            auth=(settings.SW_USER, settings.SW_PASSWORD),
            verify=False,
            json=data,
        )

    if response.status_code != 200:
        return None

    return response["results"]


def pull_network_inventory() -> List[Dict[str, Any]]:
    query = """SELECT NodeID as nodeid, IPAddress as ip, NodeName as hostname 
                FROM Orion.Nodes 
                WHERE NodeName LIKE @s OR NodeName LIKE @r OR NodeName LIKE @n"""
    parameters = {"s": "sw%", "r": "rt%", "n": "nx%"}

    # results = query_sw(query, parameters)

    results = [
        {"nodeid": 1233, "ip": "10.1.1.1", "hostname": "SWITCH1111"},
        {"nodeid": 1243, "ip": "10.1.1.2", "hostname": "SWITCH222"},
        {"nodeid": 1253, "ip": "10.1.11.3", "hostname": "SWITCH333"},
        {"nodeid": 1263, "ip": "10.11.1.4", "hostname": "SWITCH444"},
        {"nodeid": 1273, "ip": "10.1.1.5", "hostname": "SWITCH111"},
        {"nodeid": 12334, "ip": "10.1.1.14", "hostname": "SWITCH4444"},
        {"nodeid": 12434, "ip": "10.1.1.24", "hostname": "SWITCH1114"},
        {"nodeid": 12534, "ip": "10.1.1.34", "hostname": "SWITCH3333"},
        {"nodeid": 12634, "ip": "10.1.1.44", "hostname": "SWITCH1118"},
        {"nodeid": 12734, "ip": "10.1.1.54", "hostname": "SWITCH45"},
    ]

    for r in results:
        r.update({"active": True})

    return results


def pull_desktop_inventory() -> List[Dict[str, Any]]:
    query = """SELECT IPNode.IpNodeId as nodeid, IPNode.IPAddress as ip, Subnet.CIDR as cidr, IPNode.MAC as mac, IPNode.DhcpClientName as hostname
                FROM IPAM.IPNode
                INNER JOIN IPAM.Subnet ON IPNode.SubnetId = Subnet.SubnetId 
                WHERE DhcpClientName LIKE @d OR DhcpClientName LIKE @l"""
    parameters = {"d": "desktop%", "l": "laptop%"}

    # results = query_sw(query, parameters)

    results = [
        {"nodeid": 1, "ip": "10.0.1.1", "cidr": 24, "mac": "11-11-11-11-AA-A1", "hostname": "desktop00101.lab.com"},
        {"nodeid": 2, "ip": "10.0.1.2", "cidr": 24, "mac": "11-11-11-11-AA-A2", "hostname": "laptop00102.lab.com"},
        {"nodeid": 3, "ip": "10.0.1.3", "cidr": 24, "mac": "11-11-11-11-AA-A3", "hostname": "desktop00103.lab.com"},
        {"nodeid": 4, "ip": "10.0.1.4", "cidr": 24, "mac": "11-11-11-11-AA-A4", "hostname": "desktop00104.lab.com"},
        {"nodeid": 5, "ip": "10.0.1.5", "cidr": 24, "mac": "11-11-11-11-AA-A5", "hostname": "desktop00105.lab.com"},
        {"nodeid": 6, "ip": "10.0.2.1", "cidr": 24, "mac": "11-11-11-11-AA-B1", "hostname": "desktop00201.lab.com"},
        {"nodeid": 7, "ip": "10.0.2.2", "cidr": 24, "mac": "11-11-11-11-AA-B2", "hostname": "desktop00202.lab.com"},
        {"nodeid": 8, "ip": "10.0.2.3", "cidr": 24, "mac": "11-11-11-11-AA-B3", "hostname": "desktop00203.lab.com"},
        {"nodeid": 9, "ip": "10.0.2.4", "cidr": 24, "mac": "11-11-11-11-AA-B4", "hostname": "laptop00204.lab.com"},
        {"nodeid": 10, "ip": "10.0.2.5", "cidr": 24, "mac": "11-11-11-11-AA-B5", "hostname": "desktop00205.lab.com"},
    ]

    if results:
        for r in results:
            r["mac"] = r["mac"].replace("-", "").lower()
            r["hostname"] = r["hostname"].split(".")[0]

    return results


def get_site(hostname: str) -> str:
    try:
        site = re.search(r"^\D+(\d{3})", hostname)[1]
    except TypeError:
        print(f"INVALID SITE: {hostname}")
        return "999"
    return site
