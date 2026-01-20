from __future__ import annotations

from api_test_hub.config import load_project


def test_case_file_meta_applies_to_cases(tmp_path) -> None:
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

    cases_dir.joinpath("user.yaml").write_text(
        """
version: 1
case_id: DEMO-001
epic: DemoSystem
feature: User
story: Profile
severity: critical
cases:
  - name: get_user
    method: GET
    path: /users/1
""".strip(),
        encoding="utf-8",
    )

    config = load_project(project_dir)

    case = config.cases[0]
    assert case.case_id == "DEMO-001"
    assert case.epic == "DemoSystem"
    assert case.feature == "User"
    assert case.story == "Profile"
    assert case.severity == "critical"
