from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass(frozen=True)
class ResponseData:
    url: str
    method: str
    status_code: int
    headers: Dict[str, Any]
    text: str
    json: Optional[Any]


class RequestClient:
    def __init__(self, base_url: str, timeout: float = 10.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def send(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> ResponseData:
        url = f"{self.base_url}{path}"
        response = requests.request(
            method=method,
            url=url,
            params=params,
            headers=headers,
            json=json,
            data=data,
            timeout=self.timeout,
        )
        return ResponseData(
            url=url,
            method=method,
            status_code=response.status_code,
            headers=dict(response.headers),
            text=response.text,
            json=_try_json(response),
        )


def _try_json(response: requests.Response) -> Optional[Any]:
    try:
        return response.json()
    except ValueError:
        return None
