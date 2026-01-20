from __future__ import annotations

from api_test_hub.cli import main
from api_test_hub.utils import start_mock_server, stop_mock_server


def test_cli_generate(tmp_path) -> None:
    config_path = tmp_path / "demo.yaml"
    config_path.write_text(
        """
version: 1
name: demo
base_url: http://127.0.0.1:8000
cases:
  - name: get_user
    method: GET
    path: /hello
""".strip(),
        encoding="utf-8",
    )

    output_path = tmp_path / "test_generated.py"
    exit_code = main(["generate", "-c", str(config_path), "-o", str(output_path)])

    assert exit_code == 0
    assert output_path.exists()


def test_cli_run(tmp_path) -> None:
    base_url, server = start_mock_server()
    try:
        config_path = tmp_path / "demo.yaml"
        config_path.write_text(
            f"""
version: 1
name: demo
base_url: {base_url}
cases:
  - name: get_user
    method: GET
    path: /hello
""".strip(),
            encoding="utf-8",
        )

        exit_code = main(["run", "-c", str(config_path), "--timeout", "2", "--no-allure"])
        assert exit_code == 0
    finally:
        stop_mock_server(server)


def test_cli_init(tmp_path) -> None:
    target_dir = tmp_path / "template"

    exit_code = main(["init", "-o", str(target_dir)])

    assert exit_code == 0
    assert (target_dir / "README.md").exists()
    assert (target_dir / "configs" / "sample.yaml").exists()
    assert (target_dir / "requirements.txt").exists()
    assert (target_dir / "requirements-dev.txt").exists()
    assert (target_dir / ".gitignore").exists()
