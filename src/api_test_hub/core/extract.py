from __future__ import annotations

from typing import Any, Dict

from api_test_hub.core.assertions import resolve_path
from api_test_hub.core.request import ResponseData


def extract_values(response: ResponseData, mapping: Dict[str, Any]) -> Dict[str, Any]:
    extracted: Dict[str, Any] = {}
    for key, path in mapping.items():
        extracted[key] = resolve_path(response, path)
    return extracted
