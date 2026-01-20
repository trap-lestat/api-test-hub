from __future__ import annotations

import textwrap
from http.server import HTTPServer
from typing import Tuple

from api_test_hub.cases import load_cases
from api_test_hub.core import run_case


def test_extract_and_cache(http_server: Tuple[str, HTTPServer], tmp_path) -> None:
    base_url, _server = http_server
    config_text = textwrap.dedent(
        f"""
        version: 1
        name: demo
        base_url: {base_url}
        auth:
          login:
            method: POST
            path: /submit
            json:
              token: abc
            validate:
              - eq: [status_code, 201]
            extract:
              access_token: body.received.token
        cases:
          - name: get_user
            method: GET
            path: /hello
            extract:
              user_id: body.user.id
              full_body: body
          - name: get_user_again
            method: GET
            path: /users/${{user_id}}
            validate:
              - eq: [status_code, 200]
        """
    ).strip()

    config_path = tmp_path / "demo.yaml"
    config_path.write_text(config_text, encoding="utf-8")

    config, _params = load_cases(str(config_path))

    context = {}
    from api_test_hub.core.auth import perform_login

    perform_login(base_url, config.auth, config.variables, context)
    run_case(
        config.base_url,
        config.cases[0],
        context=context,
        variables=config.variables,
        auth=config.auth,
    )

    assert context["user_id"] == 7
    assert isinstance(context["full_body"], dict)

    run_case(
        config.base_url,
        config.cases[1],
        context=context,
        variables=config.variables,
        auth=config.auth,
    )
