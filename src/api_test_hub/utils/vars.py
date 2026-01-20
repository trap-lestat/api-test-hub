from __future__ import annotations

import os
import re
from typing import Any, Dict

from api_test_hub.utils.extensions import resolve_function

_VAR_PATTERN = re.compile(r"\$\{([^}]+)\}")


def interpolate(
    value: Any,
    variables: Dict[str, Any],
    allow_missing: bool = False,
    context: Dict[str, Any] | None = None,
) -> Any:
    if isinstance(value, str):
        return _interpolate_string(value, variables, allow_missing, context)
    if isinstance(value, list):
        return [interpolate(item, variables, allow_missing, context) for item in value]
    if isinstance(value, dict):
        return {
            key: interpolate(val, variables, allow_missing, context)
            for key, val in value.items()
        }
    return value


def _interpolate_string(
    value: str,
    variables: Dict[str, Any],
    allow_missing: bool,
    context: Dict[str, Any] | None,
) -> str:
    def replace(match: re.Match[str]) -> str:
        token = match.group(1)
        if token.startswith("ENV:"):
            env_key = token.split("ENV:", 1)[1]
            if env_key in os.environ:
                return os.environ[env_key]
            if allow_missing:
                return match.group(0)
            raise ValueError(f"Missing environment variable: {env_key}")
        if "=" in token:
            name, expr = token.split("=", 1)
            name = name.strip()
            expr = expr.strip()
            if not name:
                raise ValueError("Invalid assignment expression")
            result = _resolve_token(expr, variables, allow_missing)
            variables[name] = result
            if context is not None:
                context[name] = result
            return str(result)
        return str(_resolve_token(token, variables, allow_missing))

    return _VAR_PATTERN.sub(replace, value)


def _resolve_token(token: str, variables: Dict[str, Any], allow_missing: bool) -> Any:
    if token in variables:
        return variables[token]
    handled, result = resolve_function(token)
    if handled:
        return result
    if allow_missing:
        return f"${{{token}}}"
    raise ValueError(f"Missing variable: {token}")
