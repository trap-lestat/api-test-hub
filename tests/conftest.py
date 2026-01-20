from __future__ import annotations

from http.server import HTTPServer
from typing import Tuple

import pytest

from api_test_hub.utils import start_mock_server, stop_mock_server


@pytest.fixture()
def http_server() -> Tuple[str, HTTPServer]:
    base_url, server = start_mock_server()
    yield base_url, server
    stop_mock_server(server)
