from net_gsd.host import Host

from app.config import Settings, get_settings

settings: Settings = get_settings()


async def get_switch_interface_detail(host: Host) -> dict:
    """Retrieves switch description, mac, ip, cidr, vlan and desktop details"""
    result = await host.send_command(["show interfaces", "show vlan", "show mac address-table"])
    result_dict = {}

    async for record in parse_show_interface(host.hostname, result["show interfaces"]):
        result_dict.update(record)

    async for record in parse_show_vlan(result["show vlan"]["vlans"]):
        result_dict[record[0]].update(record[1])

    async for record in parse_show_mac(
        result["show mac address-table"]["mac_table"]["vlans"][str(settings.DATA_VLAN)]["mac_addresses"]
    ):
        result_dict[record[0]].update(record[1])
    return result_dict


async def get_router_interface_detail(host: Host) -> dict:
    """Retrieves router description, mac, ip, cidr"""
    result = await host.send_command(["show interfaces"])
    result_dict = {}
    async for record in parse_show_interface(host.hostname, result["show interfaces"]):
        result_dict.update(record)
    return result_dict


async def parse_show_interface(hostname: str, data: dict):
    for k, v in data.items():
        yield {
            k: {
                "description": v.get("description"),
                "mac": v.get("mac_address").replace(".", "") if v.get("mac_address") else f"{hostname}:{k}",
                "ip": v["ipv4"][next(iter(v["ipv4"]))]["ip"] if v.get("ipv4") else None,
                "cidr": v["ipv4"][next(iter(v["ipv4"]))]["prefix_length"] if v.get("ipv4") else None,
            }
        }


async def parse_show_vlan(data: dict):
    for k, v in data.items():
        if v.get("interfaces"):
            for interface in v["interfaces"]:
                yield (interface, {"vlan": k})


async def parse_show_mac(data: dict):
    for k, v in data.items():
        yield (next(iter(v["interfaces"])), {"desktop": k.replace(".", "")})
