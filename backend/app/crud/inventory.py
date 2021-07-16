from typing import List, Dict, Any, Union
import json
import logging

from edgedb import BlockingIOConnection, AsyncIOConnection
from edgedb.errors import NoDataError, ConstraintViolationError

from app.models.edge.inventory import get_shape
from app.core.utils import get_filter_str, get_filter_criteria, get_query

log = logging.getLogger("uvicorn")


def create(con: BlockingIOConnection, *, node_type: str, data: dict) -> Union[str, None]:
    try:
        result = con.query(
            f"""INSERT inventory::{node_type} {{
                {get_query(data)}
            }}
            """,
            **data,
        )
    except ConstraintViolationError as e:
        print(f"error: {data} -> {e}")
        return None
    return result


def update(con: BlockingIOConnection, *, node_type: str, data: dict) -> Union[str, None]:
    try:
        result = con.query(
            f"""UPDATE inventory::{node_type} FILTER {'.nodeid = <int64>$nodeid' if node_type == 'NetworkDevice' else '.hostname = <str>$hostname'}
            SET {{{get_query(data)}}}
            """,
            **data,
        )
    except ConstraintViolationError:
        return None
    return result


def get(
    con: BlockingIOConnection,
    *,
    node_type: str,
    filter_criteria: List[Dict[str, Any]],
    shape: str = "basic",
) -> Union[str, None]:
    try:
        result = con.query_one_json(
            f"""WITH MODULE inventory
            SELECT {node_type} {get_shape(node_type, shape)}
            FILTER {get_filter_str(filter_criteria)}""",
            **get_filter_criteria(filter_criteria),
        )
    except NoDataError:
        return None
    return result


def m_get(
    con: BlockingIOConnection,
    *,
    node_type: str,
    filter_criteria: List[Dict[str, Any]] = [],
    shape: str = "basic",
) -> Union[str, None]:
    try:
        result = con.query_json(
            f"""WITH MODULE inventory
            SELECT {node_type} {get_shape(node_type, shape)}
            {'FILTER '+ get_filter_str(filter_criteria) if filter_criteria else ''}""",
            **get_filter_criteria(filter_criteria),
        )
    except NoDataError:
        return None
    return json.loads(result)


async def acreate(con: AsyncIOConnection, *, node_type: str, data: dict) -> Union[str, None]:
    try:
        result = await con.query(
            f"""INSERT inventory::{node_type} {{
                {get_query(data)}
            }}
            """,
            **data,
        )
    except ConstraintViolationError:
        return None
    return result


async def aupdate(con: AsyncIOConnection, *, node_type: str, data: dict) -> Union[str, None]:
    try:
        print(data)
        result = await con.query(
            f"""UPDATE inventory::{node_type} FILTER {'.nodeid = <int64>$nodeid' if node_type == 'NetworkDevice' else '.hostname = <str>$hostname'}
            SET {{{get_query(data)}}}
            """,
            **data,
        )
    except ConstraintViolationError:
        return None
    return result


async def aget(
    con: AsyncIOConnection,
    *,
    node_type: str,
    filter_criteria: List[Dict[str, Any]],
    shape: str = "basic",
) -> Union[str, None]:
    try:
        result = await con.query_one_json(
            f"""SELECT inventory::{node_type} {get_shape(node_type, shape)}
            FILTER .{get_filter_str(filter_criteria)}""",
            **get_filter_criteria(filter_criteria),
        )
    except NoDataError:
        return None
    return result


async def am_get(
    con: AsyncIOConnection,
    *,
    node_type: str,
    filter_criteria: List[Dict[str, Any]] = [],
    shape: str = "basic",
) -> Union[list, None]:
    try:
        result = await con.query_json(
            f"""WITH MODULE inventory
            SELECT {node_type} {get_shape(node_type, shape)}
            {'FILTER '+ get_filter_str(filter_criteria) if filter_criteria else ''}""",
            **get_filter_criteria(filter_criteria),
        )
    except NoDataError:
        return None
    return json.loads(result)


async def acount(con: AsyncIOConnection, *, node_type: str, filter_criteria: List[Dict[str, Any]] = []):
    try:
        result = await con.query(
            f"""WITH MODULE inventory
            {'SELECT count (' + node_type + ' FILTER '+ get_filter_str(filter_criteria) +')'
            if filter_criteria else 'SELECT count(' + node_type + ')'}""",
            **get_filter_criteria(filter_criteria),
        )
    except NoDataError:
        return None
    return result[0]


async def asearch(con: AsyncIOConnection, *, search_string: str) -> Union[list, None]:
    result = {"network": [], "desktop": [], "interface": []}
    try:
        r = await con.query_json(
            f"""WITH MODULE inventory
                SELECT NetworkDevice {{
                nodeid,
                ip,
                hostname,
                site,
            }} FILTER .ip ilike '%{search_string}%' or .hostname ilike '%{search_string}%'"""
        )
    except NoDataError:
        pass
    else:
        r = json.loads(r)
        for device in r:
            result["network"].append(device)

    try:
        r = await con.query_json(
            f"""WITH MODULE inventory 
                SELECT Desktop {{
                    nodeid,
                    ip,
                    cidr,
                    mac,
                    hostname,
                    site,
                    switch := (
                        SELECT .<desktop[IS Interface].<interfaces[IS NetworkDevice] {{
                            hostname,
                            nodeid,
                            ip,
                        }}
                    ),
                    interface := .<desktop[IS Interface] {{name}}
                }}
                FILTER .ip ilike '%{search_string}%' or .hostname ilike '%{search_string}%' or .mac ilike '%{search_string}%'"""
        )
    except NoDataError:
        pass
    else:
        r = json.loads(r)
        for device in r:
            result["desktop"].append(device)

    try:
        r = await con.query_json(
            f"""WITH MODULE inventory
                SELECT Interface {{
                    switch := (
                        SELECT Interface.<interfaces[IS NetworkDevice] {{
                            nodeid,
                            hostname,
                            ip,
                            site,
                        }}
                    ),
                    name,
                    ip,
                    cidr,
                    mac,
                    vlan,
                    desktop : {{
                        hostname,
                        ip
                    }}
            }} FILTER .ip like '%{search_string}%' or .mac like '%{search_string}%'"""
        )
    except NoDataError:
        pass
    else:
        r = json.loads(r)
        for device in r:
            result["interface"].append(device)
    return result


async def update_interfaces(con: AsyncIOConnection, hostname: str, interfacelist: list):
    r = await con.query(
        """
        WITH MODULE inventory
        UPDATE NetworkDevice
        FILTER .hostname = <str>$hostname
        SET {
            interfaces += (
                FOR interface IN {
                    {json_array_unpack(<json>$interfacelist)}
                }
                UNION(
                    INSERT Interface {
                        name := re_match(r'\"(.*)\"', to_str(interface['name']))[0],
                        description := re_match(r'\"(.*)\"', to_str(interface['description']))[0],
                        mac := re_match(r'\"(.*)\"', to_str(interface['mac']))[0],
                        ip := re_match(r'\"(.*)\"', to_str(interface['ip']))[0],
                        cidr := to_int16(to_str(interface['cidr'])),
                        vlan := to_int16(to_str(interface['vlan'])),
                        desktop := (SELECT Desktop FILTER .mac = re_match(r'\"(.*)\"', to_str(interface['desktop']))[0])
                    } UNLESS CONFLICT ON .mac
                    ELSE (
                        UPDATE Interface
                        SET {
                            name := re_match(r'\"(.*)\"', to_str(interface['name']))[0],
                            description := re_match(r'\"(.*)\"', to_str(interface['description']))[0],
                            ip := re_match(r'\"(.*)\"', to_str(interface['ip']))[0],
                            cidr := to_int16(to_str(interface['cidr'])),
                            vlan := to_int16(to_str(interface['vlan'])),
                            desktop := (SELECT Desktop FILTER .mac = re_match(r'\"(.*)\"', to_str(interface['desktop']))[0])
                        }
                    )
                )
            )
        }
    """,
        hostname=hostname,
        interfacelist=json.dumps(interfacelist),
    )
