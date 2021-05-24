import re
from typing import Union, List

from httpx import Response, Client

from app.config import Settings, get_settings

settings: Settings = get_settings()


def pull_sw_inventory() -> Union[dict, List[dict]]:
    # headers = {"Content-Type": "application/json"}
    # data = {
    #     "query": "SELECT NodeID, IPAddress, NodeName, IOSImage FROM Orion.Nodes WHERE NodeName LIKE @s OR NodeName LIKE @r OR NodeName LIKE @n",
    #     "parameters": {"s": "sw%", "r": "rt%", "n": "nx%"},
    # }

    # with Client() as client:
    #     response: Response = client.get(
    #         f"https://{{settings.SW_HOST}}:17778/SolarWinds/InformationService/v3/Json/Query",
    #         headers=headers,
    #         auth=(settings.SW_USER, settings.SW_PASSWORD),
    #         verify=False,
    #         json=data,
    #     )

    # if response.status_code == 200:
    #     return response["results"]
    # else:
    #     return None
    results = [
        {"NodeID": 1233, "IPAddress": "10.1.1.1", "NodeName": "SWITCH1111", "IOSImage": "nxos9.4.2"},
        {"NodeID": 1243, "IPAddress": "10.1.1.2", "NodeName": "SWITCH222", "IOSImage": "nxos9.4.2"},
        {"NodeID": 1253, "IPAddress": "10.1.11.3", "NodeName": "SWITCH333", "IOSImage": "ios-15.1.5"},
        {"NodeID": 1263, "IPAddress": "10.11.1.4", "NodeName": "SWITCH444", "IOSImage": "ios-15.1.5"},
        {"NodeID": 1273, "IPAddress": "10.1.1.5", "NodeName": "SWITCH111", "IOSImage": "ios-15.1.5"},
        {"NodeID": 12334, "IPAddress": "10.1.1.14", "NodeName": "SWITCH4444", "IOSImage": "nxos9.4.2"},
        {"NodeID": 12434, "IPAddress": "10.1.1.24", "NodeName": "SWITCH1114", "IOSImage": "nxos9.4.2"},
        {"NodeID": 12534, "IPAddress": "10.1.1.34", "NodeName": "SWITCH3333", "IOSImage": "ios-15.1.5"},
        {"NodeID": 12634, "IPAddress": "10.1.1.44", "NodeName": "SWITCH1118", "IOSImage": "ios-15.1.5"},
        {"NodeID": 12734, "IPAddress": "10.1.1.54", "NodeName": "SWITCH45", "IOSImage": "ios-15.1.5"},
    ]
    return [{k.lower(): v for k, v in r.items()} for r in results]
    # return results


def get_site(hostname: str) -> str:
    try:
        site = re.search(r"^\D+(\d{3})", hostname)[1]
    except TypeError:
        print(f"INVALID SITE: {hostname}")
        return "999"
    return site
