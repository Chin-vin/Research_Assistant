# =========================================================
# tests/unit/test_router.py
# =========================================================

from agents.router import (
    retrieval_router_agent
)


def test_router():

    state = {
        "query": "AI"
    }

    result = retrieval_router_agent(
        state
    )

    assert (
        "routing"
        in result
    )