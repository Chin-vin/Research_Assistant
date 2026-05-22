# =========================================================
# tests/unit/test_pdf_retriever.py
# =========================================================

from agents.pdf_retriever import (
    pdf_retriever_agent
)


def test_pdf_retriever():

    state = {

        "query":
            "AI",

        "subqueries":
            [],

        "retrieved_docs":
            [],

        "routing":
            {
                "retrieval_mode":
                    "pdf_only"
            },

        "vector_db":
            None
    }

    result = pdf_retriever_agent(
        state
    )

    assert (
        "retrieved_docs"
        in result
    )