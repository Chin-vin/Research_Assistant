# =========================================================
# tests/integration/test_human_approval.py
# =========================================================

from agents.human_approval import (
    human_approval_agent
)


def test_human_approval():

    state = {

        "analysis":
            {

                "summary":
                    "AI Summary",

                "key_findings":
                    ["Finding"]
            },

        "validation":
            {

                "confidence_score":
                    0.95,

                "research_sufficient":
                    True
            }
    }

    result = human_approval_agent(
        state
    )

    assert (
        result[
            "awaiting_human_approval"
        ]
        is True
    )