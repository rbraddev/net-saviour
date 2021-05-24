from typing import Any, Dict, List

# from app.models.edge.inventory import get_query_model


def get_type(value: Any) -> str:
    if type(value) == bool:
        return "<bool>"
    elif type(value) == str:
        return "<str>"
    elif type(value) == int:
        return "<int64>"
    else:
        raise ValueError("Type not found.")


def get_query(data: Dict[str, Any]) -> str:
    query_list = [f"{k} := {get_type(v)}${k}" for k, v in data.items()]
    query_expr = ", ".join(query_list)
    return query_expr


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


# def get_criteria(criteria: List[Dict[str, Any]]) -> str:
#     if len(criteria) == 1:
#         criteria_str = f".{[k +' = +'+get_type(v)+'$'+k for k, v in criteria[0].items()][0]}"

#     return criteria_str

# def query_builder(*, model: str, criteria: List[Dict[str, Any]] = [], data: dict = {}) -> str:
#     return f"""{get_query_model(model)} {'FILTER ' + get_criteria(criteria) if criteria else ''}"""
