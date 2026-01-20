from __future__ import annotations

from http.server import HTTPServer
from typing import Tuple

from api_test_hub.cases import load_cases
from api_test_hub.core import run_case
from api_test_hub.utils import start_mock_server, stop_mock_server


def test_mock_example_sample_config(monkeypatch) -> None:
    base_url, server = start_mock_server()
    try:
        monkeypatch.setenv("MOCK_BASE_URL", base_url)
        config, _params = load_cases("examples/mock_server/sample.yaml")
        context = {}
        for case in config.cases:
            run_case(
                config.base_url,
                case,
                variables=config.variables,
                context=context,
                auth=config.auth,
            )
        assert context["user_id"] == 42
        assert context["user_name"] == "lei"
    finally:
        stop_mock_server(server)
