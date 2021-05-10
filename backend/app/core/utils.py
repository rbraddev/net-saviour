from typing import Any, Dict, List


def get_type(value: Any) -> str:
    if type(value) == bool:
        return "<bool>"
    elif type(value) == str:
        return "<str>"
    elif type(value) == int:
        return "<int64>"
    else:
        raise ValueError("Type not found.")


def get_shape(data: Dict[str, Any]) -> str:
    shape_list = [f"{k} := {get_type(v)}${k}" for k, v in data.items()]
    shape_expr = ", ".join(shape_list)
    return shape_expr


def get_filter_str(data: List[Dict[str, Any]]) -> str:
    filter_string = ""
    for item in data:
        for k, v in item.items():
            if k == "oper":
                filter_string += f" {v} "
            else:
                filter_string += f"{k} = {get_type(v)}${k}"
    return filter_string


def get_filter_criteria(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    criteria = {}
    for d in data:
        for k, v in d.items():
            if k != "oper":
                criteria.update({k: v})
    return criteria
