shapes = {
    "NetworkDevice": {
        "basic": """{
            nodeid,
            hostname,
            site,
            ip,
            device_type,
            platform,
            active,
        }""",
        "extended": """{
            nodeid,
            hostname,
            site,
            ip,
            device_type,
            platform,
            active,
            interfaces : {
                name,
                description,
                ip,
                cidr,
                mac,
                vlan,
                desktop: {
                    nodeid,
                    hostname,
                    ip,
                    cidr,
                    mac,
                }
            }           
        }""",
    },
    "Desktop": {
        "basic": """{
            nodeid,
            hostname,
            site,
            ip,
            cidr,
            mac
        }""",
    },
}


def get_shape(node_type: str, shape: str) -> str:
    return shapes[node_type].get(shape)
