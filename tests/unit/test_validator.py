# =========================================================
# tests/unit/test_validator.py
# =========================================================

from agents.validator import (
    validation_agent
)


def test_validator():

    state = {

        "analysis":
            {

                "summary":
                    "AI Research",

                "confidence_score":
                    0.9
            },

        "errors":
            []
    }

    result = validation_agent(
        state
    )

    assert (
        "validation"
        in result
    )