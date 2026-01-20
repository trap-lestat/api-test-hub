from __future__ import annotations

from pathlib import Path


def generate_pytest_file(config_path: str | Path, output_path: str | Path) -> Path:
    config_file = Path(config_path)
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    content = _render_template(config_file)
    output_file.write_text(content, encoding="utf-8")
    return output_file


def generate_pytest_project_file(
    project_dir: str | Path, output_path: str | Path
) -> Path:
    project_path = Path(project_dir)
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    content = _render_project_template(project_path)
    output_file.write_text(content, encoding="utf-8")
    return output_file


def _render_template(config_file: Path) -> str:
    config_literal = repr(str(config_file))
    return (
        "from __future__ import annotations\n\n"
        "import allure\n"
        "import pytest\n\n"
        "from api_test_hub.cases import load_cases\n"
        "from api_test_hub.core import run_case\n"
        "from api_test_hub.core.auth import perform_login\n\n"
        + _render_allure_helpers()
        + f"CONFIG_PATH = {config_literal}\n\n"
        "config, params = load_cases(CONFIG_PATH)\n"
        "context = {}\n"
        "perform_login(config.base_url, config.auth, config.variables, context)\n\n"
        "@pytest.mark.parametrize(\"case\", params)\n"
        "def test_api_cases(case):\n"
        "    allure.dynamic.title(case.name)\n"
        "    _apply_allure_meta(case)\n"
        "    run_case(config.base_url, case, variables=config.variables, context=context, auth=config.auth)\n"
    )


def _render_project_template(project_dir: Path) -> str:
    project_literal = repr(str(project_dir))
    return (
        "from __future__ import annotations\n\n"
        "import allure\n"
        "import pytest\n\n"
        "from api_test_hub.cases import build_pytest_params\n"
        "from api_test_hub.config import load_project\n"
        "from api_test_hub.core import run_case\n"
        "from api_test_hub.core.auth import perform_login\n\n"
        + _render_allure_helpers()
        + f"PROJECT_DIR = {project_literal}\n\n"
        "config = load_project(PROJECT_DIR)\n"
        "params = build_pytest_params(config.cases)\n"
        "context = {}\n"
        "perform_login(config.base_url, config.auth, config.variables, context)\n\n"
        "@pytest.mark.parametrize(\"case\", params)\n"
        "def test_api_cases(case):\n"
        "    allure.dynamic.title(case.name)\n"
        "    _apply_allure_meta(case)\n"
        "    run_case(config.base_url, case, variables=config.variables, context=context, auth=config.auth)\n"
    )


def _render_allure_helpers() -> str:
    return (
        "def _apply_allure_meta(case):\n"
        "    if case.case_id:\n"
        "        allure.dynamic.label(\"case_id\", case.case_id)\n"
        "    if case.epic:\n"
        "        allure.dynamic.epic(case.epic)\n"
        "    if case.feature:\n"
        "        allure.dynamic.feature(case.feature)\n"
        "    if case.story:\n"
        "        allure.dynamic.story(case.story)\n"
        "    if case.severity:\n"
        "        allure.dynamic.severity(case.severity)\n"
        "\n"
    )
