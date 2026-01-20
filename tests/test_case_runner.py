from __future__ import annotations

import textwrap
from http.server import HTTPServer
from typing import Tuple

from api_test_hub.cases import load_cases
from api_test_hub.core import run_case


def test_run_case_from_config(http_server: Tuple[str, HTTPServer], tmp_path) -> None:
    base_url, _server = http_server
    config_text = textwrap.dedent(
        f"""
        version: 1
        name: demo
        base_url: {base_url}
        cases:
          - name: get_user
            method: GET
            path: /hello
            validate:
              - eq: [status_code, 200]
              - contains: [body.message, "hell"]
          - name: post_user
            method: POST
            path: /submit
            json:
              name: lei
            validate:
              - eq: [status_code, 201]
              - eq: [body.received.name, "lei"]
          - name: retry_user
            method: GET
            path: /hello
            retries: 1
            retry_delay: 0
            validate:
              - eq: [status_code, 200]
        """
    ).strip()

    config_path = tmp_path / "demo.yaml"
    config_path.write_text(config_text, encoding="utf-8")

    config, params = load_cases(str(config_path))

    assert [param.id for param in params] == ["get_user", "post_user", "retry_user"]

    context = {}
    for case in config.cases:
        run_case(
            config.base_url,
            case,
            context=context,
            variables=config.variables,
            auth=config.auth,
            dbs=config.db,
        )
