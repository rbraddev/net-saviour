from typing import Union, List

from httpx import AsyncClient, Response

from app.config import Settings, get_settings

settings:Settings = get_settings()


def pull_sw_inventory() -> Union[dict, List[dict]]:
    # headers = {"Content-Type": "application/json"}
    # data = {
    #     "query": "SELECT NodeID, IPAddress, NodeName, IOSImage FROM Orion.Nodes WHERE NodeName LIKE @s OR NodeName LIKE @r OR NodeName LIKE @n",
	#     "parameters": {
	#         "s": "sw%",
	# 	    "r": "rt%",
	# 	    "n": "nx%"
	#     }
    # }
    
    # async with AsyncClient() as client:
    #     response: Response = client.get(
    #         f"https://{{settings.SW_HOST}}:17778/SolarWinds/InformationService/v3/Json/Query",
    #         headers=headers, auth=(settings.SW_USER, settings.SW_PASSWORD), verify=False, json=data
    #     )
    
    # if response.status_code == 200:
    #     return response["results"]
    # else:
    #     return None
    results = [
	    {
		    "NodeID": 123,
			"IPAddress": "10.1.1.1",
			"NodeName": "SWITCH1",
			"IOSImage": "nxos9.4.2"
		},
        {
		    "NodeID": 124,
			"IPAddress": "10.1.1.2",
			"NodeName": "SWITCH2",
			"IOSImage": "nxos9.4.2"
		},
        {
		    "NodeID": 125,
			"IPAddress": "10.1.1.3",
			"NodeName": "SWITCH3",
			"IOSImage": "ios-15.1.5"
		},
        {
		    "NodeID": 126,
			"IPAddress": "10.1.1.4",
			"NodeName": "SWITCH4",
			"IOSImage": "ios-15.1.5"
		},
        {
		    "NodeID": 127,
			"IPAddress": "10.1.1.5",
			"NodeName": "SWITCH5",
			"IOSImage": "ios-15.1.5"
		},
	]

    return results