import ast
from typing import List

from .types import Filter


def build_filter_dict(query_params: dict) -> dict:
    """
    Build a filter dictionary from query parameters.

    Args:
        query_params (dict): A dictionary of query parameters.

    Returns:
        dict: A dictionary suitable for Django ORM filtering.
    """
    filter_dict = {}
    for key, value in query_params.items():
        if "." in key:
            field_name, filter_type = key.split(".", 1)
            if filter_type.upper() in Filter.__members__:
                if isinstance(value,str):
                    try:
                        filter_dict[f"{field_name}__{Filter[filter_type.upper()].value}"] = ast.literal_eval(value)
                    except ValueError:
                        filter_dict[f"{field_name}__{Filter[filter_type.upper()].value}"] = value
                else:
                    filter_dict[f"{field_name}__{Filter[filter_type.upper()].value}"] = value
            else:
                filter_dict[key] = value
    return filter_dict


def build_query_str(query_params: dict) -> str:
    items = []
    for key, value in query_params.items():
        if "." in key:
            items.append(f"{key}={value}")
    return "&".join(items)

def build_filters_template_dict(filter: dict) -> dict:
    results = {}
    for key, value in filter.items():
        results[key.split("__")[0]] = value
    return results

def split_and_strip(content: str) -> List[str]:
    """
    Split content text in to a List[str] for further processing.

    Returns:
        List of lines
    """
    lines = [
        line.strip(" ").replace("\xa0", "").replace("\xc2", "")
        for line in content.strip(" ").replace("\r\n", "\n").split("\n")
    ]
    return [line for line in lines if line]