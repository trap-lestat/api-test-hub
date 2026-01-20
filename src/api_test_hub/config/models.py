from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass(frozen=True)
class CaseConfig:
    name: str
    method: str
    path: str
    case_id: str = ""
    epic: str = ""
    feature: str = ""
    story: str = ""
    severity: str = ""
    params: Dict[str, Any] = field(default_factory=dict)
    headers: Dict[str, Any] = field(default_factory=dict)
    json: Dict[str, Any] = field(default_factory=dict)
    data: Dict[str, Any] = field(default_factory=dict)
    validate: List[Dict[str, Any]] = field(default_factory=list)
    retries: int = 0
    retry_delay: float = 0.0
    extract: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class APISuiteConfig:
    version: int
    name: str
    base_url: str
    cases: List[CaseConfig]
    variables: Dict[str, Any] = field(default_factory=dict)
    auth: Dict[str, Any] = field(default_factory=dict)
