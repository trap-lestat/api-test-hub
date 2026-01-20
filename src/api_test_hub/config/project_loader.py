from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List

from api_test_hub.config.loader import ConfigError, _build_case, _ensure_dict, _load_file
from api_test_hub.config.models import APISuiteConfig, CaseConfig
from api_test_hub.utils.vars import interpolate


_PROJECT_FILES = ["project.yaml", "project.yml", "project.json"]


def load_project(project_dir: str | Path) -> APISuiteConfig:
    root = Path(project_dir)
    if not root.exists():
        raise ConfigError(f"Project directory not found: {root}")

    project_file = _find_project_file(root)
    if project_file is None:
        raise ConfigError("Project config not found (project.yaml/yml/json)")

    project_raw = _load_file(project_file)
    _validate_project(project_raw)

    variables = project_raw.get("variables", {})
    if not isinstance(variables, dict):
        raise ConfigError("variables must be a dict")

    cases_dir = project_raw.get("cases_dir", "cases")
    case_files = project_raw.get("case_files")
    case_paths = _resolve_case_files(root, cases_dir, case_files)

    cases: List[CaseConfig] = []
    for case_path in case_paths:
        cases.extend(_load_case_file(case_path, variables))

    return APISuiteConfig(
        version=int(project_raw["version"]),
        name=str(project_raw["name"]),
        base_url=str(project_raw["base_url"]),
        cases=cases,
        variables=variables,
        auth=_ensure_dict(project_raw.get("auth")),
        db=_ensure_dict(project_raw.get("db")),
    )


def _find_project_file(root: Path) -> Path | None:
    for name in _PROJECT_FILES:
        path = root / name
        if path.exists():
            return path
    return None


def _validate_project(data: Dict[str, Any]) -> None:
    required = ["version", "name", "base_url"]
    for field in required:
        if field not in data:
            raise ConfigError(f"Project missing required field: {field}")


def _resolve_case_files(
    root: Path, cases_dir: str, case_files: Any
) -> List[Path]:
    if case_files is None:
        return _discover_case_files(root / cases_dir)

    if not isinstance(case_files, list):
        raise ConfigError("case_files must be a list")

    resolved: List[Path] = []
    for item in case_files:
        resolved.append((root / cases_dir / str(item)).resolve())
    return resolved


def _discover_case_files(cases_dir: Path) -> List[Path]:
    if not cases_dir.exists():
        raise ConfigError(f"cases_dir not found: {cases_dir}")
    patterns = ["*.yaml", "*.yml", "*.json"]
    files: List[Path] = []
    for pattern in patterns:
        files.extend(sorted(cases_dir.rglob(pattern)))
    if not files:
        raise ConfigError(f"No case files found in: {cases_dir}")
    return files


def _load_case_file(path: Path, project_vars: Dict[str, Any]) -> Iterable[CaseConfig]:
    raw = _load_file(path)
    if "base_url" in raw:
        raise ConfigError(
            f"Case file should not define base_url (use project config): {path}"
        )
    if "cases" not in raw or not isinstance(raw["cases"], list):
        raise ConfigError(f"Case file missing cases list: {path}")

    file_meta = {
        "case_id": str(raw.get("case_id", "")),
        "epic": str(raw.get("epic", "")),
        "feature": str(raw.get("feature", "")),
        "story": str(raw.get("story", "")),
        "severity": str(raw.get("severity", "")),
    }

    case_vars = raw.get("variables", {})
    if case_vars is None:
        case_vars = {}
    if not isinstance(case_vars, dict):
        raise ConfigError("case file variables must be a dict")

    merged_vars = {**project_vars, **case_vars}
    interpolated = interpolate(raw, merged_vars, allow_missing=True)

    cases: List[CaseConfig] = []
    for case in interpolated["cases"]:
        merged_case = {
            **file_meta,
            **{key: value for key, value in case.items() if value is not None},
        }
        cases.append(_build_case(merged_case))
    return cases
