from __future__ import annotations

import ast
import textwrap

from api_test_hub.cases import generate_pytest_file


def test_generate_pytest_file(tmp_path) -> None:
    config_text = textwrap.dedent(
        """
        version: 1
        name: demo
        base_url: http://127.0.0.1:8000
        cases:
          - name: get_user
            method: GET
            path: /hello
        """
    ).strip()

    config_path = tmp_path / "demo.yaml"
    config_path.write_text(config_text, encoding="utf-8")

    output_path = tmp_path / "test_generated.py"
    generated = generate_pytest_file(config_path, output_path)

    content = generated.read_text(encoding="utf-8")
    ast.parse(content)

    assert "def test_api_cases" in content
    assert "context = {}" in content
    assert str(config_path) in content
