shapes = {
    "NetworkDevice": {
        "basic": """{
            nodeid,
            hostname,
            ip,
            active,
        }""",
    },
    "Desktop": {
        "basic": """{
            nodeid,
            hostname,
            ip,
            cidr,
            mac
        }""",
    },
}


def get_shape(node_type: str, shape: str) -> str:
    return shapes[node_type].get(shape)
