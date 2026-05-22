# =========================================================
# tests/unit/test_supervisor.py
# =========================================================

from agents.supervisor import (
    supervisor_agent
)


def test_supervisor_routes():

    state = {
        "query": "AI"
    }

    result = supervisor_agent(
        state
    )

    assert (
        result["next_agent"]
        == "decomposer"
    )