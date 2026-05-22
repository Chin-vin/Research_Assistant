# =========================================================
# tests/unit/test_arxiv_retriever.py
# =========================================================

from agents.arxiv_retriever import (
    arxiv_retriever_agent
)


def test_arxiv_retriever():

    state = {

        "query":
            "AI",

        "subqueries":
            ["Machine Learning"],

        "retrieved_docs":
            [],

        "routing":
            {
                "retrieval_mode":
                    "arxiv_only"
            }
    }

    result = arxiv_retriever_agent(
        state
    )

    assert (
        "retrieved_docs"
        in result
    )