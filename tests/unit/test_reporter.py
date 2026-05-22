# =========================================================
# tests/unit/test_reporter.py
# =========================================================

from agents.reporter import (
    reporting_agent
)


def test_reporter():

    state = {

        "query":
            "AI",

        "analysis":
            {

                "summary":
                    "AI Summary",

                "key_findings":
                    ["AI Finding"],

                "dynamic_sections":
                    []
            }
    }

    result = reporting_agent(
        state
    )

    assert (
        "report"
        in result
    )