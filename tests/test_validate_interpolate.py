from __future__ import annotations

import textwrap

from api_test_hub.config import load_config
from api_test_hub.core import run_case
from api_test_hub.utils import start_mock_server, stop_mock_server


def test_validate_interpolates_variables(tmp_path) -> None:
    base_url, server = start_mock_server()
    try:
        config_text = textwrap.dedent(
            f"""
            version: 1
            name: demo
            base_url: {base_url}
            variables:
              username: lei
            cases:
              - name: check_user
                method: GET
                path: /hello
                validate:
                  - eq: [body.user.id, 7]
                  - contains: [body.message, "hell"]
            """
        ).strip()

        config_path = tmp_path / "demo.yaml"
        config_path.write_text(config_text, encoding="utf-8")

        config = load_config(config_path)
        context = {}
        run_case(
            config.base_url,
            config.cases[0],
            variables=config.variables,
            context=context,
            auth=config.auth,
        )
    finally:
        stop_mock_server(server)
