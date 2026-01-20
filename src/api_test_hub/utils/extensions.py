from __future__ import annotations

import random
import string
import time
import uuid
from typing import Any, Callable, Dict, List, Tuple


_ExtFn = Callable[[List[Any]], Any]
_FUNCTIONS: Dict[str, _ExtFn] = {}


def register_function(name: str, func: _ExtFn) -> None:
    _FUNCTIONS[name] = func


def resolve_function(token: str) -> Tuple[bool, Any]:
    name, args = _parse_call(token)
    if name is None:
        return False, None
    if name not in _FUNCTIONS:
        raise ValueError(f"Unknown function: {name}")
    return True, _FUNCTIONS[name](args)


def _parse_call(token: str) -> Tuple[str | None, List[Any]]:
    if not token.endswith(")") or "(" not in token:
        return None, []
    name, arg_str = token.split("(", 1)
    name = name.strip()
    arg_str = arg_str[:-1].strip()
    if not name:
        return None, []
    if not arg_str:
        return name, []
    return name, _parse_args(arg_str)


def _parse_args(arg_str: str) -> List[Any]:
    raw_args = [part.strip() for part in arg_str.split(",")]
    parsed: List[Any] = []
    for raw in raw_args:
        if not raw:
            continue
        if (raw.startswith("\"") and raw.endswith("\"")) or (
            raw.startswith("'") and raw.endswith("'")
        ):
            parsed.append(raw[1:-1])
            continue
        parsed.append(_parse_number(raw))
    return parsed


def _parse_number(value: str) -> Any:
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value


# Built-in extension functions

def _random_int(args: List[Any]) -> int:
    if len(args) != 2:
        raise ValueError("random_int expects 2 arguments: min, max")
    return random.randint(int(args[0]), int(args[1]))


def _random_str(args: List[Any]) -> str:
    length = int(args[0]) if args else 8
    alphabet = string.ascii_letters + string.digits
    return "".join(random.choice(alphabet) for _ in range(length))


def _timestamp(args: List[Any]) -> int:
    return int(time.time())


def _uuid(args: List[Any]) -> str:
    return str(uuid.uuid4())


register_function("random_int", _random_int)
register_function("random_str", _random_str)
register_function("timestamp", _timestamp)
register_function("uuid", _uuid)
