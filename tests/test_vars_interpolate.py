from __future__ import annotations

import re

from api_test_hub.utils.vars import interpolate


def test_interpolate_allow_missing() -> None:
    data = {"path": "/users/${user_id}", "name": "${missing}"}
    result = interpolate(data, {"user_id": 7}, allow_missing=True)

    assert result["path"] == "/users/7"
    assert result["name"] == "${missing}"


def test_interpolate_functions() -> None:
    data = {
        "rand": "${random_int(1,10)}",
        "stamp": "${timestamp()}",
        "uuid": "${uuid()}",
        "tag": "${random_str(6)}",
    }
    result = interpolate(data, {}, allow_missing=False)

    assert 1 <= int(result["rand"]) <= 10
    assert int(result["stamp"]) > 0
    assert re.match(r"^[0-9a-f-]{36}$", result["uuid"]) is not None
    assert len(result["tag"]) == 6
