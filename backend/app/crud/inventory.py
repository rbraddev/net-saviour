from typing import List, Dict, Any, Union
import json

from edgedb import BlockingIOConnection, AsyncIOConnection
from edgedb.errors import NoDataError, ConstraintViolationError

from app.models.edge.inventory import get_shape
from app.core.utils import get_filter_str, get_filter_criteria, get_query


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
    return result


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


async def asearch(con: AsyncIOConnection, *, search_string: str) -> Union[list, None]:
    result = []
    try:
        r = await con.query_json(
            f"""WITH MODULE inventory
                SELECT NetworkDevice {{
                id,
                nodeid,
                ip,
                hostname,
                interfaces : {{
                    name,
                    ip,
                    mac,
                    desktop: {{
                        hostname,
                        ip
                    }}
                }}
            }} FILTER .ip ilike '%{search_string}%' or .hostname ilike '%{search_string}%'"""
        )
    except NoDataError:
        pass
    else:
        r = json.loads(r)
        for device in r:
            result.append(device)

    try:
        r = await con.query_json(
            f"""WITH MODULE inventory 
                SELECT Desktop {{
                    id,
                    ip,
                    mac,
                    hostname,
                    switch := (
                        SELECT NetworkDevice {{
                            hostname,
                            nodeid,
                            ip
                        }} FILTER .interfaces.desktop.ip like '%{search_string}%' or .interfaces.desktop.hostname like '%{search_string}%'
                    ),
                    interface := (
                        SELECT Interface {{
                            name
                        }} FILTER .desktop.ip like '%{search_string}%' or .desktop.hostname like '%{search_string}%'
                    )
                }}
                FILTER .ip ilike '%{search_string}%' or .hostname ilike '%{search_string}%' or .mac like '%{search_string}%'"""
        )
    except NoDataError:
        pass
    else:
        r = json.loads(r)
        for device in r:
            result.append(device)

    # try:
    r = await con.query_json(
        f"""WITH MODULE inventory
            SELECT Interface {{
                switch := (
                    SELECT Interface.<interfaces[IS NetworkDevice] {{
                        hostname
                    }}
                ),
                name,
                ip,
                desktop : {{
                    hostname,
                    ip
                }}
        }} FILTER .ip like '%{search_string}%' or .mac like '%{search_string}%'"""
    )
    # except NoDataError:
    #     pass
    # else:
    #     r = json.loads(r)
    #     for device in r:
    #         result.append(device)
    return result
