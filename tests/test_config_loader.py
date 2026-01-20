import textwrap

import pytest

from api_test_hub.config import ConfigError, load_config


def test_load_config_interpolates_variables(tmp_path):
    config_text = textwrap.dedent(
        """
        version: 1
        name: demo
        base_url: https://api.example.com
        variables:
          user_id: 7
        cases:
          - name: get_user
            method: get
            path: /users/${user_id}
        """
    ).strip()

    config_path = tmp_path / "demo.yaml"
    config_path.write_text(config_text, encoding="utf-8")

    config = load_config(config_path)

    assert config.cases[0].path == "/users/7"
    assert config.cases[0].method == "GET"


def test_load_config_case_meta(tmp_path):
    config_text = textwrap.dedent(
        """
        version: 1
        name: demo
        base_url: https://api.example.com
        cases:
          - name: health
            method: GET
            path: /health
            case_id: API-001
            epic: DemoSystem
            feature: Health
            story: BasicCheck
            severity: critical
        """
    ).strip()

    config_path = tmp_path / "demo.yaml"
    config_path.write_text(config_text, encoding="utf-8")

    config = load_config(config_path)

    case = config.cases[0]
    assert case.case_id == "API-001"
    assert case.epic == "DemoSystem"
    assert case.feature == "Health"
    assert case.story == "BasicCheck"
    assert case.severity == "critical"


def test_load_config_missing_required_field(tmp_path):
    config_text = textwrap.dedent(
        """
        version: 1
        name: demo
        base_url: https://api.example.com
        """
    ).strip()

    config_path = tmp_path / "demo.yaml"
    config_path.write_text(config_text, encoding="utf-8")

    with pytest.raises(ConfigError):
        load_config(config_path)
