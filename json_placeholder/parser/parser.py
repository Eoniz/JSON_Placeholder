import json

from typing import Any, Callable, Dict, List, Optional

from json_placeholder.utils.random import float_between, int_bewteen, one_of


def _handle_string(yaml_string_obj: Dict[str, Any]) -> str:
    values = yaml_string_obj.get("values", ["a", "b", "c"])
    return one_of(values)


def _handle_int(yaml_int_obj: Dict[str, Any]) -> int:
    min = yaml_int_obj.get("min", 0)
    max = yaml_int_obj.get("max", 10)
    return int_bewteen(min, max)


def _handle_float(yaml_float_obj: Dict[str, Any]) -> float:
    min = yaml_float_obj.get("min", 0.0)
    max = yaml_float_obj.get("max", 1.0)
    return float_between(min, max)


def _handle_object(yaml_object_obj: Dict[str, Any]) -> Dict[str, Any]:
    fields = yaml_object_obj.get("fields", [])
    constructed_items: Dict[str, Any] = {}

    for field in fields:
        if "key" not in field:
            continue
        if "type" not in field:
            continue

        type_ = field.get("type")
        key_ = field.get("key")

        handler = HANDLERS.get(type_, lambda _: None)
        constructed_value = handler(field)
        constructed_items[key_] = constructed_value
            
    return constructed_items


def _handle_array(yaml_array_obj: Dict[str, Any]) -> List[Any]:
    array = yaml_array_obj.get("array", None)
    if array is None:
        return []
    
    type_ = array.get("type", None)

    if type_ is None:
        return []

    min_ = yaml_array_obj.get("min", 0)
    max_ = yaml_array_obj.get("max", 10)
    nb_items = int_bewteen(min_, max_)
    constructed_items: List[Any] = []

    for _ in range(nb_items):
        constructed_value = None
        handler = HANDLERS.get(type_, lambda _: None)
        constructed_value = handler(array)

        if constructed_value is not None:
            constructed_items.append(constructed_value)

    return constructed_items


HANDLERS: Dict[str, Callable[[Optional[Dict[str, Any]]], Any]] = {
    "string": _handle_string,
    "int": _handle_int,
    "float": _handle_float,
    "object": _handle_object,
    "array": _handle_array
}


def parse_yaml(yaml_obj: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    constructed_object: Dict[str, Any] = {}

    print(yaml_obj)
    for key, value in yaml_obj.items():
        type_ = value.get("type", None)
        if not type_:
            continue
        
        constructed_value = None
        handler = HANDLERS.get(type_, lambda _: None)
        constructed_value = handler(value)

        if constructed_value is not None:
            constructed_object[key] = constructed_value
    
    print(json.dumps(constructed_object, sort_keys=True, indent=4))
    return constructed_object
