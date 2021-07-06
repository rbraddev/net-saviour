import re
from typing import *

from httpx import Response, AsyncClient

from app.config import Settings, get_settings

settings: Settings = get_settings()


platform = {"rt": "router", "sw": "switch", "nx": "nexus"}


async def query_sw(query: str, parameters: dict) -> List[Dict[str, Any]]:
    headers = {"Content-Type": "application/json"}
    data = {
        "query": query,
        "parameters": parameters,
    }

    with AsyncClient() as client:
        response: Response = await client.get(
            f"https://{{settings.SW_HOST}}:17778/SolarWinds/InformationService/v3/Json/Query",
            headers=headers,
            auth=(settings.SW_USER, settings.SW_PASSWORD),
            verify=False,
            json=data,
        )

    if response.status_code != 200:
        return None

    return response["results"]


async def pull_network_inventory() -> List[Dict[str, Any]]:
    query = """SELECT NodeID as nodeid, IPAddress as ip, NodeName as hostname 
                FROM Orion.Nodes 
                WHERE NodeName LIKE @s OR NodeName LIKE @r OR NodeName LIKE @n"""
    parameters = {"s": "sw%", "r": "rt%", "n": "nx%"}

    # results = await query_sw(query, parameters)

    results = [
        {"nodeid": 1, "ip": "10.0.0.1", "hostname": "RT1001"},
        {"nodeid": 2, "ip": "10.0.0.2", "hostname": "RT1002"},
        {"nodeid": 3, "ip": "10.0.0.3", "hostname": "RT2001"},
        {"nodeid": 4, "ip": "10.0.0.4", "hostname": "RT2002"},
        {"nodeid": 5, "ip": "10.0.0.5", "hostname": "RT1011"},
        {"nodeid": 6, "ip": "10.0.0.6", "hostname": "RT1021"},
        {"nodeid": 7, "ip": "10.0.0.7", "hostname": "RT1031"},
        {"nodeid": 8, "ip": "10.0.0.8", "hostname": "SW1011"},
        {"nodeid": 9, "ip": "10.0.0.9", "hostname": "SW1021"},
        {"nodeid": 10, "ip": "10.0.0.10", "hostname": "SW1031"},
        {"nodeid": 11, "ip": "10.0.0.11", "hostname": "NX1001"},
        {"nodeid": 12, "ip": "10.0.0.12", "hostname": "NX2001"},
    ]

    for r in results:
        r.update({"active": True, "platform": platform.get(r["hostname"][:2].lower(), "undefined")})

    return results


async def pull_desktop_inventory() -> List[Dict[str, Any]]:
    query = """SELECT IPNode.IpNodeId as nodeid, IPNode.IPAddress as ip, Subnet.CIDR as cidr, IPNode.MAC as mac, IPNode.DhcpClientName as hostname
                FROM IPAM.IPNode
                INNER JOIN IPAM.Subnet ON IPNode.SubnetId = Subnet.SubnetId 
                WHERE DhcpClientName LIKE @d OR DhcpClientName LIKE @l"""
    parameters = {"d": "desktop%", "l": "laptop%"}

    # results = await query_sw(query, parameters)

    results = [
        {"nodeid": 1, "ip": "10.101.10.1", "cidr": 24, "mac": "52-54-00-0A-BB-9D", "hostname": "PC1011.lab.local"},
        {"nodeid": 2, "ip": "10.101.10.2", "cidr": 24, "mac": "52-54-00-0D-02-EB", "hostname": "PC1012.lab.local"},
        {"nodeid": 3, "ip": "10.102.10.1", "cidr": 24, "mac": "52-54-00-03-66-DE", "hostname": "PC1021.lab.local"},
        {"nodeid": 4, "ip": "10.102.10.2", "cidr": 24, "mac": "52-54-00-14-94-BB", "hostname": "PC1022.lab.local"},
        {"nodeid": 5, "ip": "10.103.10.1", "cidr": 24, "mac": "52-54-00-06-25-67", "hostname": "PC1031.lab.local"},
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
