from __future__ import annotations

from typing import Iterable, List, Tuple

import pytest

from api_test_hub.config import APISuiteConfig, CaseConfig, load_config


def build_pytest_params(cases: Iterable[CaseConfig]) -> List[pytest.ParamSpec]:
    return [pytest.param(case, id=case.name) for case in cases]


def load_cases(path: str) -> Tuple[APISuiteConfig, List[pytest.ParamSpec]]:
    config = load_config(path)
    return config, build_pytest_params(config.cases)
