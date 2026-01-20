from __future__ import annotations

from http.server import HTTPServer
from typing import Tuple

from api_test_hub.config import load_project
from api_test_hub.core import run_case


def test_load_project_from_folder(http_server: Tuple[str, HTTPServer], tmp_path) -> None:
    base_url, _server = http_server
    project_dir = tmp_path / "project"
    cases_dir = project_dir / "cases"
    cases_dir.mkdir(parents=True)

    project_dir.joinpath("project.yaml").write_text(
        f"""
version: 1
name: demo_project
base_url: {base_url}
variables:
  user_id: 7
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
    validate:
      - eq: [status_code, 200]
""".strip(),
        encoding="utf-8",
    )

    config = load_project(project_dir)

    assert config.base_url == base_url
    assert len(config.cases) == 1

    context = {}
    run_case(
        config.base_url,
        config.cases[0],
        variables=config.variables,
        context=context,
        auth=config.auth,
    )
