from __future__ import annotations

import base64
from typing import Any, Dict, Optional

from api_test_hub.config.models import CaseConfig
from api_test_hub.core.assertions import assert_response
from api_test_hub.core.extract import extract_values
from api_test_hub.core.request import RequestClient
from api_test_hub.utils.vars import interpolate


def apply_auth(case: CaseConfig, auth: Dict[str, Any] | None) -> CaseConfig:
    if not auth:
        return case

    headers = dict(case.headers)

    auth_type = str(auth.get("type", "")).lower()
    if auth_type == "bearer":
        token = auth.get("token")
        if token:
            headers["Authorization"] = f"Bearer {token}"
    elif auth_type == "cookie":
        cookie_data = auth.get("cookies", {})
        if isinstance(cookie_data, dict):
            cookie_pairs = [f"{key}={value}" for key, value in cookie_data.items()]
            existing = headers.get("Cookie")
            if existing:
                headers["Cookie"] = f"{existing}; " + "; ".join(cookie_pairs)
            else:
                headers["Cookie"] = "; ".join(cookie_pairs)
    elif auth_type == "basic":
        username = auth.get("username")
        password = auth.get("password")
        if username is not None and password is not None:
            token = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode(
                "utf-8"
            )
            headers["Authorization"] = f"Basic {token}"

    return CaseConfig(
        name=case.name,
        method=case.method,
        path=case.path,
        case_id=case.case_id,
        epic=case.epic,
        feature=case.feature,
        story=case.story,
        severity=case.severity,
        params=case.params,
        headers=headers,
        json=case.json,
        data=case.data,
        validate=case.validate,
        retries=case.retries,
        retry_delay=case.retry_delay,
        extract=case.extract,
        validate_db=case.validate_db,
    )


def perform_login(
    base_url: str,
    auth: Dict[str, Any],
    variables: Dict[str, Any],
    context: Dict[str, Any],
    timeout: float = 10.0,
    logger: Optional[object] = None,
) -> None:
    login = auth.get("login")
    if not login:
        return

    runtime_vars = {**variables, **context}
    interpolated = interpolate(login, runtime_vars, allow_missing=True, context=context)

    case = _build_login_case(interpolated)
    client = RequestClient(base_url, timeout=timeout)
    response = client.send(
        method=case.method,
        path=case.path,
        params=case.params,
        headers=case.headers,
        json=case.json,
        data=case.data,
    )

    if logger is not None:
        logger.info("login response status=%s", response.status_code)

    if case.validate:
        assert_response(response, case.validate)
    if case.extract:
        context.update(extract_values(response, case.extract))
        return


def _build_login_case(login: Dict[str, Any]) -> CaseConfig:
    return CaseConfig(
        name=str(login.get("name", "auth_login")),
        method=str(login.get("method", "POST")).upper(),
        path=str(login.get("path", "/login")),
        params=_ensure_dict(login.get("params")),
        headers=_ensure_dict(login.get("headers")),
        json=_ensure_dict(login.get("json")),
        data=_ensure_dict(login.get("data")),
        validate=_ensure_list(login.get("validate")),
        extract=_ensure_dict(login.get("extract")),
    )


def _ensure_dict(value: Any) -> Dict[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ValueError("Expected a dict")
    return value


def _ensure_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError("Expected a list")
    return value
