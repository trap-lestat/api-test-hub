from __future__ import annotations

from pathlib import Path


def generate_pytest_file(config_path: str | Path, output_path: str | Path) -> Path:
    config_file = Path(config_path)
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    content = _render_template(config_file)
    output_file.write_text(content, encoding="utf-8")
    return output_file


def _render_template(config_file: Path) -> str:
    config_literal = repr(str(config_file))
    return (
        "from __future__ import annotations\n\n"
        "import pytest\n\n"
        "from api_test_hub.cases import load_cases\n"
        "from api_test_hub.core import run_case\n\n"
        f"CONFIG_PATH = {config_literal}\n\n"
        "config, params = load_cases(CONFIG_PATH)\n"
        "context = {}\n\n"
        "@pytest.mark.parametrize(\"case\", params)\n"
        "def test_api_cases(case):\n"
        "    run_case(config.base_url, case, variables=config.variables, context=context)\n"
    )
