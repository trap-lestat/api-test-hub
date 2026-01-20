from __future__ import annotations

import re
from typing import Any, Dict, Iterable

from api_test_hub.core.request import ResponseData


class AssertionErrorDetail(AssertionError):
    pass


def assert_response(response: ResponseData, validations: Iterable[Dict[str, Any]]) -> None:
    for rule in validations:
        if not isinstance(rule, dict) or len(rule) != 1:
            raise AssertionErrorDetail(f"Invalid validation rule: {rule}")
        operator, payload = next(iter(rule.items()))
        if operator == "eq":
            _assert_eq(response, payload)
        elif operator == "not_eq":
            _assert_not_eq(response, payload)
        elif operator == "gt":
            _assert_gt(response, payload)
        elif operator == "gte":
            _assert_gte(response, payload)
        elif operator == "lt":
            _assert_lt(response, payload)
        elif operator == "lte":
            _assert_lte(response, payload)
        elif operator == "in":
            _assert_in(response, payload)
        elif operator == "not_in":
            _assert_not_in(response, payload)
        elif operator == "exists":
            _assert_exists(response, payload)
        elif operator == "regex":
            _assert_regex(response, payload)
        elif operator == "contains":
            _assert_contains(response, payload)
        else:
            raise AssertionErrorDetail(f"Unsupported operator: {operator}")


def _assert_eq(response: ResponseData, payload: Any) -> None:
    path, expected = _ensure_pair(payload, "eq")
    actual = resolve_path(response, path)
    if actual != expected:
        raise AssertionErrorDetail(f"eq failed: {path}={actual!r} expected={expected!r}")


def _assert_not_eq(response: ResponseData, payload: Any) -> None:
    path, expected = _ensure_pair(payload, "not_eq")
    actual = resolve_path(response, path)
    if actual == expected:
        raise AssertionErrorDetail(
            f"not_eq failed: {path}={actual!r} expected != {expected!r}"
        )


def _assert_gt(response: ResponseData, payload: Any) -> None:
    path, expected = _ensure_pair(payload, "gt")
    actual = resolve_path(response, path)
    if actual is None or actual <= expected:
        raise AssertionErrorDetail(f"gt failed: {path}={actual!r} expected > {expected!r}")


def _assert_gte(response: ResponseData, payload: Any) -> None:
    path, expected = _ensure_pair(payload, "gte")
    actual = resolve_path(response, path)
    if actual is None or actual < expected:
        raise AssertionErrorDetail(
            f"gte failed: {path}={actual!r} expected >= {expected!r}"
        )


def _assert_lt(response: ResponseData, payload: Any) -> None:
    path, expected = _ensure_pair(payload, "lt")
    actual = resolve_path(response, path)
    if actual is None or actual >= expected:
        raise AssertionErrorDetail(f"lt failed: {path}={actual!r} expected < {expected!r}")


def _assert_lte(response: ResponseData, payload: Any) -> None:
    path, expected = _ensure_pair(payload, "lte")
    actual = resolve_path(response, path)
    if actual is None or actual > expected:
        raise AssertionErrorDetail(
            f"lte failed: {path}={actual!r} expected <= {expected!r}"
        )


def _assert_in(response: ResponseData, payload: Any) -> None:
    path, expected = _ensure_pair(payload, "in")
    actual = resolve_path(response, path)
    if _value_in(actual, expected) is False:
        raise AssertionErrorDetail(f"in failed: {path}={actual!r} missing {expected!r}")


def _assert_not_in(response: ResponseData, payload: Any) -> None:
    path, expected = _ensure_pair(payload, "not_in")
    actual = resolve_path(response, path)
    if _value_in(actual, expected) is True:
        raise AssertionErrorDetail(
            f"not_in failed: {path}={actual!r} should not contain {expected!r}"
        )


def _assert_exists(response: ResponseData, payload: Any) -> None:
    path = _ensure_path(payload, "exists")
    actual = resolve_path(response, path)
    if actual is None:
        raise AssertionErrorDetail(f"exists failed: {path} not found")


def _assert_regex(response: ResponseData, payload: Any) -> None:
    path, pattern = _ensure_pair(payload, "regex")
    actual = resolve_path(response, path)
    if actual is None or re.search(str(pattern), str(actual)) is None:
        raise AssertionErrorDetail(
            f"regex failed: {path}={actual!r} pattern={pattern!r}"
        )


def _assert_contains(response: ResponseData, payload: Any) -> None:
    path, expected = _ensure_pair(payload, "contains")
    actual = resolve_path(response, path)
    if actual is None:
        raise AssertionErrorDetail(f"contains failed: {path} is None")
    if str(expected) not in str(actual):
        raise AssertionErrorDetail(
            f"contains failed: {path}={actual!r} missing {expected!r}"
        )


def resolve_path(response: ResponseData, path: Any) -> Any:
    if path == "status_code":
        return response.status_code
    if path == "body":
        return response.json if response.json is not None else response.text
    if isinstance(path, str) and path.startswith("body."):
        if response.json is None:
            return None
        return _get_nested_value(response.json, path.split(".", 1)[1])
    return None


def _ensure_pair(payload: Any, name: str) -> tuple[Any, Any]:
    if not isinstance(payload, list) or len(payload) != 2:
        raise AssertionErrorDetail(f"{name} rule must be a list of [path, expected]")
    return payload[0], payload[1]


def _ensure_path(payload: Any, name: str) -> Any:
    if isinstance(payload, list) and len(payload) == 1:
        return payload[0]
    if isinstance(payload, str):
        return payload
    raise AssertionErrorDetail(f"{name} rule must be a path or [path]")


def _value_in(actual: Any, expected: Any) -> bool | None:
    if actual is None:
        return False
    if isinstance(actual, (list, tuple, set)):
        return expected in actual
    if isinstance(expected, (list, tuple, set)):
        return actual in expected
    if isinstance(actual, str):
        return str(expected) in actual
    return None


def _get_nested_value(data: Any, path: str) -> Any:
    current = data
    for segment in path.split("."):
        if isinstance(current, dict) and segment in current:
            current = current[segment]
        else:
            return None
    return current
