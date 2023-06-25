import random
import time
from typing import Any, Dict, List, Literal, Optional, Union

import orjson


def generate_keyname() -> str:
    return str(int(time.time())) + random.randbytes(16).hex()


def json_decode(data: Optional[Any]) -> Union[List, Dict, Literal[False]]:
    try:
        data = orjson.loads(data)
    except orjson.JSONDecodeError:
        data = False
    return data if isinstance(data, (list, dict)) else False


def json_encode(data: Optional[Any]) -> Union[bytes, Literal[False]]:
    try:
        data = orjson.dumps(data)
    except orjson.JSONEncodeError:
        data = False
    return data


def to_str(value: Any) -> str:
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, (int, float)) and value == 0:
        return "0"
    if not value:
        return ""
    if isinstance(value, (dict, list)):
        return json_encode(value)
    try:
        value = str(value)
        return value
    except ValueError:
        return ""


def to_timestamp(value: str, str_format: str = "%Y-%m-%d %H:%M:%S") -> int:
    try:
        timestamp = int(time.mktime(time.strptime(value, str_format)))
        if timestamp:
            return timestamp
        return int(time.time())
    except ValueError:
        return int(time.time())


def to_int(value: Any) -> int:
    if not value:
        return 0
    try:
        value = int(float(value))
        return value
    except (ValueError, TypeError):
        return 0


def to_bool(value: Any) -> bool:
    if isinstance(value, str):
        if value.lower().strip() == "false":
            return False
    if value:
        return bool(value)
    return False


def to_decimal(value: Any, length: Optional[int] = None) -> float:
    if not value:
        return 0.00
    try:
        if isinstance(value, str):
            if "," in value:
                value = value.replace(",", ".")
        value = round(float(value), length) if length else float(value)
        return value
    except (ValueError, TypeError):
        return 0.00


def to_len(value: Any) -> int:
    if not value:
        return 0
    try:
        res = len(value)
    except TypeError:
        res = 0
    return res
