device_create_query = {
    "NetworkDevice": """
        nodeid := <int64>$nodeid,
        hostname := <str>$hostname,
        ip := <str>$ip,
        """,
    "Desktop": """
        hostname := <str>$hostname, 
        ip := <str>$ip,
        switch := (
            SELECT inventory::NetworkDevice 
            FILTER .nodeid = <int64>$nodeid
        ), switch_port := <str>$switch_port
        """,
}


def get_device_create_query(node_type: str) -> str:
    return device_create_query.get(node_type)
