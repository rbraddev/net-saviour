from typing import List, Dict, Any, Union

from edgedb import BlockingIOConnection, AsyncIOConnection
from edgedb.errors import NoDataError, ConstraintViolationError

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
    except ConstraintViolationError:
        return None
    return result


def update(con: BlockingIOConnection, *, node_type: str, data: dict) -> Union[str, None]:
    try:
        result = con.query(
            f"""UPDATE inventory::{node_type} FILTER .nodeid = <int64>$nodeid
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
    fields: list = ["ip", "hostname"],
) -> Union[str, None]:
    try:
        result = con.query_one_json(
            f"""SELECT inventory::{node_type} {'{'+','.join(fields)+'}'}
            FILTER .{get_filter_str(filter_criteria)}""",
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
    fields: list = ["ip", "hostname"],
) -> Union[str, None]:
    try:
        result = con.query_json(
            f"""SELECT inventory::{node_type} {'{'+','.join(fields)+'}'}
            {'FILTER .'+ get_filter_str(filter_criteria) if filter_criteria else ''}""",
            **get_filter_criteria(filter_criteria),
        )
    except NoDataError:
        return None
    return result


async def aget(
    con: AsyncIOConnection,
    *,
    node_type: str,
    filter_criteria: List[Dict[str, Any]],
    fields: list = ["ip", "hostname"],
) -> Union[str, None]:
    try:
        result = await con.query_one_json(
            f"""SELECT inventory::{node_type} {'{'+','.join(fields)+'}'}
            FILTER .{get_filter_str(filter_criteria)}""",
            **get_filter_criteria(filter_criteria),
        )
    except NoDataError:
        return None
    return result
