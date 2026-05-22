# =========================================================
# tests/unit/test_analysis.py
# =========================================================

from agents.analyzer import (
    analysis_agent
)


def test_analysis():

    state = {

        "query":
            "AI",

        "retrieved_docs":
            [

                {

                    "title":
                        "AI Research",

                    "content":
                        "AI improves healthcare.",

                    "url":
                        "https://example.com"
                }
            ]
    }

    result = analysis_agent(
        state
    )

    assert (
        "analysis"
        in result
    )