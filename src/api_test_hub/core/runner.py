from __future__ import annotations

import json
import time
from typing import Any, Dict, Optional

from api_test_hub.config.models import CaseConfig
from api_test_hub.core.assertions import AssertionErrorDetail, assert_response
from api_test_hub.core.extract import extract_values
from api_test_hub.core.request import RequestClient, ResponseData
from api_test_hub.utils.vars import interpolate


def run_case(
    base_url: str,
    case: CaseConfig,
    timeout: float = 10.0,
    logger: Optional[object] = None,
    variables: Optional[Dict[str, Any]] = None,
    context: Optional[Dict[str, Any]] = None,
) -> ResponseData:
    runtime_vars: Dict[str, Any] = {}
    if variables:
        runtime_vars.update(variables)
    if context:
        runtime_vars.update(context)

    runtime_base_url = str(interpolate(base_url, runtime_vars))
    runtime_case = _interpolate_case(case, runtime_vars)

    client = RequestClient(runtime_base_url, timeout=timeout)
    attempts = max(case.retries + 1, 1)
    last_error: Optional[Exception] = None

    for attempt in range(1, attempts + 1):
        if logger is not None:
            logger.info(
                "request case=%s attempt=%s/%s method=%s path=%s params=%s headers=%s json=%s data=%s",
                case.name,
                attempt,
                attempts,
                runtime_case.method,
                runtime_case.path,
                runtime_case.params,
                runtime_case.headers,
                runtime_case.json,
                runtime_case.data,
            )

        response = client.send(
            method=runtime_case.method,
            path=runtime_case.path,
            params=runtime_case.params,
            headers=runtime_case.headers,
            json=runtime_case.json,
            data=runtime_case.data,
        )
        _attach_allure_request(runtime_base_url, runtime_case, attempt, attempts)
        _attach_allure_response(response)

        if logger is not None:
            body_preview = response.json if response.json is not None else response.text
            logger.info(
                "response case=%s status=%s headers=%s body=%s",
                case.name,
                response.status_code,
                response.headers,
                body_preview,
            )

        try:
            _attach_allure_validate(runtime_case.validate)
            assert_response(response, runtime_case.validate)
            if context is not None and runtime_case.extract:
                extracted = extract_values(response, runtime_case.extract)
                context.update(extracted)
                _attach_allure_extract(extracted)
            return response
        except AssertionErrorDetail as exc:
            last_error = exc
            _attach_allure_validate_result(str(exc))
            if attempt < attempts and case.retry_delay > 0:
                time.sleep(case.retry_delay)

    raise AssertionErrorDetail(
        f"case failed after {attempts} attempts: {case.name} {case.method} {case.path} ({last_error})"
    )


def _interpolate_case(case: CaseConfig, variables: Dict[str, Any]) -> CaseConfig:
    return CaseConfig(
        name=case.name,
        method=case.method,
        path=str(interpolate(case.path, variables)),
        params=interpolate(case.params, variables),
        headers=interpolate(case.headers, variables),
        json=interpolate(case.json, variables),
        data=interpolate(case.data, variables),
        validate=case.validate,
        retries=case.retries,
        retry_delay=case.retry_delay,
        extract=case.extract,
    )


def _attach_allure_request(
    base_url: str, case: CaseConfig, attempt: int, attempts: int
) -> None:
    payload = {
        "case": case.name,
        "attempt": f"{attempt}/{attempts}",
        "method": case.method,
        "url": f"{base_url}{case.path}",
        "headers": case.headers,
        "params": case.params,
        "json": case.json,
        "data": case.data,
    }
    _allure_attach("request", payload)


def _attach_allure_response(response: ResponseData) -> None:
    payload = {
        "method": response.method,
        "url": response.url,
        "status_code": response.status_code,
        "headers": response.headers,
        "body": response.json if response.json is not None else response.text,
    }
    _allure_attach("response", payload)


def _attach_allure_extract(extracted: Dict[str, Any]) -> None:
    _allure_attach("extract", extracted)


def _attach_allure_validate(validations: Any) -> None:
    _allure_attach("validate", validations)


def _attach_allure_validate_result(message: str) -> None:
    _allure_attach("validate_result", {"status": "failed", "message": message})


def _allure_attach(name: str, content: Any) -> None:
    try:
        import allure

        if isinstance(content, (dict, list)):
            allure.attach(
                json.dumps(content, ensure_ascii=False, indent=2),
                name=name,
                attachment_type=allure.attachment_type.JSON,
            )
        else:
            allure.attach(
                str(content),
                name=name,
                attachment_type=allure.attachment_type.TEXT,
            )
    except Exception:
        return
