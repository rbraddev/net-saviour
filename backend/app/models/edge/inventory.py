shapes = {
    "NetworkDevice": {
        "import": """{
            nodeid,
            ip,
            hostname,
            active,
            device_type,
            platform
        }""",
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
        "import": """{
            nodeid,
            ip,
            cidr,
            mac,
            hostname
        }""",
        "basic": """{
            nodeid,
            hostname,
            site,
            ip,
            cidr,
            mac
        }""",
        "extended": """{
            nodeid,
            ip,
            cidr,
            mac,
            hostname,
            site,
            switch := (
                SELECT .<desktop[IS Interface].<interfaces[IS NetworkDevice] {
                    hostname,
                    nodeid,
                    ip,
                    interface := array_agg(Desktop.<desktop[IS Interface] {name})[0]
                }
            ),
        }""",
    },
    "Interface": {
        "extended": """{
            switch := (
                SELECT Interface.<interfaces[IS NetworkDevice] {
                    nodeid,
                    hostname,
                    ip,
                    site,
                }
            ),
            name,
            ip,
            cidr,
            mac,
            vlan,
            desktop : {
                hostname,
                ip
        }"""
    },
}


def get_shape(node_type: str, shape: str) -> str:
    return shapes[node_type].get(shape)
