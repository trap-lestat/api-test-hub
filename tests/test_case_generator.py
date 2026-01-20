from __future__ import annotations

import ast
import textwrap

from api_test_hub.cases import generate_pytest_file, generate_pytest_project_file


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
    assert "perform_login" in content
    assert "auth=config.auth" in content
    assert "dbs=config.db" in content
    assert "allure.dynamic.title" in content
    assert "_apply_allure_meta" in content
    assert str(config_path) in content


def test_generate_pytest_project_file(tmp_path) -> None:
    project_dir = tmp_path / "project"
    cases_dir = project_dir / "cases"
    cases_dir.mkdir(parents=True)
    project_dir.joinpath("project.yaml").write_text(
        """
version: 1
name: demo
base_url: http://127.0.0.1:8000
cases_dir: cases
""".strip(),
        encoding="utf-8",
    )
    cases_dir.joinpath("health.yaml").write_text(
        """
version: 1
cases:
  - name: health
    method: GET
    path: /hello
""".strip(),
        encoding="utf-8",
    )

    output_path = tmp_path / "test_project_generated.py"
    generated = generate_pytest_project_file(project_dir, output_path)

    content = generated.read_text(encoding="utf-8")
    ast.parse(content)
    assert "load_project" in content
    assert "perform_login" in content
    assert "auth=config.auth" in content
    assert "dbs=config.db" in content
    assert "allure.dynamic.title" in content
    assert "_apply_allure_meta" in content
