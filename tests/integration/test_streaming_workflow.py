# =========================================================
# tests/integration/test_streaming_workflow.py
# =========================================================

from workflow.graph import (
    graph
)


def test_streaming():

    initial_state = {

        "thread_id":
            "stream-test",

        "query":
            "AI Research",

        "subqueries":
            [],

        "retrieved_docs":
            [],

        "analysis":
            {},

        "validation":
            {},

        "report":
            {},

        "citations":
            [],

        "errors":
            [],

        "workflow_complete":
            False,

        "next_agent":
            "supervisor",

        "vector_db":
            None,

        "routing":
            {},

        "pdf_uploaded":
            False,

        "awaiting_human_approval":
            False,

        "human_feedback":
            ""
    }

    events = graph.stream(
        initial_state
    )

    assert events is not None