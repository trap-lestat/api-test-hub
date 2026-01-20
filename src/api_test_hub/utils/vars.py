from __future__ import annotations

import os
import re
from typing import Any, Dict

_VAR_PATTERN = re.compile(r"\$\{([^}]+)\}")


def interpolate(value: Any, variables: Dict[str, Any], allow_missing: bool = False) -> Any:
    if isinstance(value, str):
        return _interpolate_string(value, variables, allow_missing)
    if isinstance(value, list):
        return [interpolate(item, variables, allow_missing) for item in value]
    if isinstance(value, dict):
        return {key: interpolate(val, variables, allow_missing) for key, val in value.items()}
    return value


def _interpolate_string(value: str, variables: Dict[str, Any], allow_missing: bool) -> str:
    def replace(match: re.Match[str]) -> str:
        token = match.group(1)
        if token.startswith("ENV:"):
            env_key = token.split("ENV:", 1)[1]
            if env_key in os.environ:
                return os.environ[env_key]
            if allow_missing:
                return match.group(0)
            raise ValueError(f"Missing environment variable: {env_key}")
        if token in variables:
            return str(variables[token])
        if allow_missing:
            return match.group(0)
        raise ValueError(f"Missing variable: {token}")

    return _VAR_PATTERN.sub(replace, value)
