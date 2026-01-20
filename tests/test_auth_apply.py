from __future__ import annotations

from api_test_hub.config.models import CaseConfig
from api_test_hub.core.auth import apply_auth


def test_apply_auth_bearer() -> None:
    case = CaseConfig(name="demo", method="GET", path="/hello")
    auth = {"type": "bearer", "token": "abc"}

    updated = apply_auth(case, auth)

    assert updated.headers["Authorization"] == "Bearer abc"


def test_apply_auth_cookie() -> None:
    case = CaseConfig(name="demo", method="GET", path="/hello")
    auth = {"type": "cookie", "cookies": {"sid": "123", "uid": "u1"}}

    updated = apply_auth(case, auth)

    assert "sid=123" in updated.headers["Cookie"]
    assert "uid=u1" in updated.headers["Cookie"]
