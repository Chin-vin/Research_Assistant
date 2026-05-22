# =========================================================
# tests/unit/test_decomposer.py
# =========================================================

from agents.decomposer import (
    decomposition_agent
)


def test_decomposition():

    state = {
        "query": "AI in Healthcare"
    }

    result = decomposition_agent(
        state
    )

    assert (
        "subqueries"
        in result
    )

    assert isinstance(
        result["subqueries"],
        list
    )