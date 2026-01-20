from __future__ import annotations

from api_test_hub.utils.vars import interpolate


def test_extension_assignment_cached() -> None:
    context = {}
    result = interpolate(
        {"token": "${access_token=uuid()}"},
        {},
        context=context,
    )

    assert "access_token" in context
    assert result["token"] == context["access_token"]
