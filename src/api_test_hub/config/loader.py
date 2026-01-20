from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import yaml

from api_test_hub.config.models import APISuiteConfig, CaseConfig
from api_test_hub.utils.vars import interpolate


class ConfigError(ValueError):
    pass


def load_config(path: str | Path) -> APISuiteConfig:
    raw = _load_file(path)
    _validate_top_level(raw)

    variables = raw.get("variables", {})
    if not isinstance(variables, dict):
        raise ConfigError("variables must be a dict")

    interpolated = interpolate(raw, variables, allow_missing=True)
    _validate_top_level(interpolated)

    cases = [_build_case(case) for case in interpolated["cases"]]
    return APISuiteConfig(
        version=int(interpolated["version"]),
        name=str(interpolated["name"]),
        base_url=str(interpolated["base_url"]),
        cases=cases,
        variables=variables,
    )


def _load_file(path: str | Path) -> Dict[str, Any]:
    file_path = Path(path)
    if not file_path.exists():
        raise ConfigError(f"Config file not found: {file_path}")

    suffix = file_path.suffix.lower()
    if suffix in {".yaml", ".yml"}:
        return _load_yaml(file_path)
    if suffix == ".json":
        return _load_json(file_path)

    raise ConfigError("Config file must be .yaml, .yml, or .json")


def _load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ConfigError("YAML config must be a mapping")
    return data


def _load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ConfigError("JSON config must be an object")
    return data


def _validate_top_level(data: Dict[str, Any]) -> None:
    required = ["version", "name", "base_url", "cases"]
    for field in required:
        if field not in data:
            raise ConfigError(f"Missing required field: {field}")

    if not isinstance(data["cases"], list):
        raise ConfigError("cases must be a list")


def _build_case(case: Dict[str, Any]) -> CaseConfig:
    required = ["name", "method", "path"]
    for field in required:
        if field not in case:
            raise ConfigError(f"Case missing required field: {field}")

    method = str(case["method"]).upper()
    return CaseConfig(
        name=str(case["name"]),
        method=method,
        path=str(case["path"]),
        params=_ensure_dict(case.get("params")),
        headers=_ensure_dict(case.get("headers")),
        json=_ensure_dict(case.get("json")),
        data=_ensure_dict(case.get("data")),
        validate=_ensure_list(case.get("validate")),
        retries=_ensure_int(case.get("retries", 0)),
        retry_delay=_ensure_float(case.get("retry_delay", 0.0)),
        extract=_ensure_dict(case.get("extract")),
    )


def _ensure_dict(value: Any) -> Dict[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ConfigError("Expected a dict")
    return value


def _ensure_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ConfigError("Expected a list")
    return value


def _ensure_int(value: Any) -> int:
    if isinstance(value, bool):
        raise ConfigError("Expected an int")
    if isinstance(value, int):
        return value
    if value is None:
        return 0
    raise ConfigError("Expected an int")


def _ensure_float(value: Any) -> float:
    if isinstance(value, bool):
        raise ConfigError("Expected a float")
    if isinstance(value, (int, float)):
        return float(value)
    if value is None:
        return 0.0
    raise ConfigError("Expected a float")
