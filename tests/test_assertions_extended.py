from __future__ import annotations

import pytest

from api_test_hub.core import AssertionErrorDetail, assert_response
from api_test_hub.core.request import ResponseData


def test_extended_assertions_success() -> None:
    response = ResponseData(
        url="http://localhost/hello",
        method="GET",
        status_code=200,
        headers={},
        text="ok",
        json={
            "id": 42,
            "name": "lei",
            "count": 5,
            "tags": ["alpha", "beta"],
        },
    )

    assert_response(
        response,
        [
            {"eq": ["status_code", 200]},
            {"not_eq": ["body.name", "tom"]},
            {"gt": ["body.count", 3]},
            {"gte": ["body.count", 5]},
            {"lt": ["body.count", 10]},
            {"lte": ["body.count", 5]},
            {"in": ["body.tags", "alpha"]},
            {"not_in": ["body.tags", "gamma"]},
            {"exists": ["body.id"]},
            {"regex": ["body.name", "^l.*"]},
            {"eq": ["body.tags[0]", "alpha"]},
        ],
    )


def test_extended_assertions_failure() -> None:
    response = ResponseData(
        url="http://localhost/hello",
        method="GET",
        status_code=200,
        headers={},
        text="ok",
        json={"count": 1, "name": "lei"},
    )

    with pytest.raises(AssertionErrorDetail):
        assert_response(response, [{"gt": ["body.count", 5]}])
