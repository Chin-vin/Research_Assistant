# =========================================================
# tests/unit/test_web_retriever.py
# =========================================================

from agents.web_retriever import (
    web_retriever_agent
)


def test_web_retriever():

    state = {

        "query":
            "AI",

        "subqueries":
            ["AI applications"],

        "retrieved_docs":
            [],

        "routing":
            {
                "retrieval_mode":
                    "web_only"
            }
    }

    result = web_retriever_agent(
        state
    )

    assert (
        "retrieved_docs"
        in result
    )