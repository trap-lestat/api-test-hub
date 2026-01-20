from __future__ import annotations

from typing import Tuple

from http.server import HTTPServer

import pytest

from api_test_hub.core import AssertionErrorDetail, RequestClient, assert_response


def test_request_client_get_and_assertions(http_server: Tuple[str, HTTPServer]) -> None:
    base_url, _server = http_server
    client = RequestClient(base_url)
    response = client.send("GET", "/hello")

    assert_response(
        response,
        [
            {"eq": ["status_code", 200]},
            {"eq": ["body.user.id", 7]},
            {"contains": ["body.message", "hell"]},
        ],
    )


def test_request_client_post_json(http_server: Tuple[str, HTTPServer]) -> None:
    base_url, _server = http_server
    client = RequestClient(base_url)
    response = client.send("POST", "/submit", json={"name": "lei"})

    assert response.status_code == 201
    assert response.json["received"]["name"] == "lei"


def test_assertion_failure_message(http_server: Tuple[str, HTTPServer]) -> None:
    base_url, _server = http_server
    client = RequestClient(base_url)
    response = client.send("GET", "/hello")

    with pytest.raises(AssertionErrorDetail):
        assert_response(response, [{"eq": ["status_code", 500]}])
