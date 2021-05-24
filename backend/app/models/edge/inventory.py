shape_model = {
    "network_get": """inventory::NetworkDevice {
        nodeid := <int64>$nodeid,
        hostname := <str>$hostname,
        ip := <str>$ip,
    }""",
    "Desktop": """
        hostname := <str>$hostname, 
        ip := <str>$ip,
        switch := (
            SELECT inventory::NetworkDevice 
            FILTER .nodeid = <int64>$nodeid
        ), switch_port := <str>$switch_port
        """,
}


def get_shape(shape: str) -> str:
    return shape_model.get(shape)
