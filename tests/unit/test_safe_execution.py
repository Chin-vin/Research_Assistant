# =========================================================
# tests/unit/test_safe_execution.py
# =========================================================

from utils.safe_execution import (
    safe_execute
)


def failing_agent(state):

    raise Exception(
        "Test Error"
    )


def test_safe_execution():

    result = safe_execute(
        failing_agent,
        {}
    )

    assert (
        "errors"
        in result
    )