from __future__ import annotations

from http.server import HTTPServer
from typing import Tuple

from api_test_hub.core.auth import perform_login


def test_perform_login_extracts_token(http_server: Tuple[str, HTTPServer]) -> None:
    base_url, _server = http_server
    auth = {
        "login": {
            "method": "POST",
            "path": "/submit",
            "json": {"token": "abc"},
            "validate": [{"eq": ["status_code", 201]}],
            "extract": {"access_token": "body.received.token"},
        }
    }
    variables = {}
    context = {}

    perform_login(base_url, auth, variables, context)

    assert context["access_token"] == "abc"
