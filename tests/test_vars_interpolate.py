from __future__ import annotations

from api_test_hub.utils.vars import interpolate


def test_interpolate_allow_missing() -> None:
    data = {"path": "/users/${user_id}", "name": "${missing}"}
    result = interpolate(data, {"user_id": 7}, allow_missing=True)

    assert result["path"] == "/users/7"
    assert result["name"] == "${missing}"
