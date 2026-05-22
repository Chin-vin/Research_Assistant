# # # =========================================================
# # # tests/integration/test_full_workflow.py
# # # =========================================================

# # from workflow.graph import (
# #     graph
# # )


# # def test_complete_workflow():

# #     initial_state = {

# #         "thread_id":
# #             "test-thread",

# #         "query":
# #             "Impact of AI on Healthcare",

# #         "subqueries":
# #             [],

# #         "retrieved_docs":
# #             [],

# #         "analysis":
# #             {},

# #         "validation":
# #             {},

# #         "report":
# #             {},

# #         "citations":
# #             [],

# #         "errors":
# #             [],

# #         "workflow_complete":
# #             False,

# #         "next_agent":
# #             "supervisor",

# #         "vector_db":
# #             None,

# #         "routing":
# #             {},

# #         "pdf_uploaded":
# #             False,

# #         "awaiting_human_approval":
# #             False,

# #         "human_feedback":
# #             ""
# #     }

# #     result = graph.invoke(
# #         initial_state
# #     )

# #     assert result is not None
# # =========================================================
# # tests/integration/test_full_workflow.py
# # =========================================================

# from workflow.graph import graph


# def test_complete_workflow():

#     initial_state = {

#         # -----------------------------------------
#         # THREAD / SESSION
#         # -----------------------------------------

#         "thread_id":
#             "test-thread",

#         # -----------------------------------------
#         # QUERY
#         # -----------------------------------------

#         "query":
#             "Impact of AI on Healthcare",

#         "subqueries":
#             [],

#         # -----------------------------------------
#         # RETRIEVAL
#         # -----------------------------------------

#         "retrieved_docs":
#             [],

#         "vector_db":
#             None,

#         "routing":
#             {
#                 "retrieval_mode":
#                     "web_only"
#             },

#         "pdf_uploaded":
#             False,

#         # -----------------------------------------
#         # ANALYSIS
#         # -----------------------------------------

#         "analysis":
#             {},

#         "validation":
#             {},

#         "report":
#             {},

#         "citations":
#             [],

#         # -----------------------------------------
#         # HUMAN IN LOOP
#         # -----------------------------------------

#         "awaiting_human_approval":
#             False,

#         "human_feedback":
#             "",

#         # -----------------------------------------
#         # EXECUTION
#         # -----------------------------------------

#         "errors":
#             [],

#         "retries":
#             {},

#         "workflow_complete":
#             False,

#         "critical_error":
#             False,

#         "next_agent":
#             "supervisor",
#     }

#     result = graph.invoke(
#         initial_state
#     )

#     # -----------------------------------------
#     # BASIC ASSERTIONS
#     # -----------------------------------------

#     assert result is not None

#     assert isinstance(
#         result,
#         dict
#     )

#     # -----------------------------------------
#     # NO CRITICAL FAILURE
#     # -----------------------------------------

#     assert not result.get(
#         "critical_error",
#         False
#     )

#     # -----------------------------------------
#     # ANALYSIS EXISTS
#     # -----------------------------------------

#     assert "analysis" in result

#     # -----------------------------------------
#     # VALIDATION EXISTS
#     # -----------------------------------------

#     assert "validation" in result

#     # -----------------------------------------
#     # REPORT EXISTS
#     # -----------------------------------------

#     assert "report" in result

#     # -----------------------------------------
#     # ERRORS SHOULD BE EMPTY
#     # -----------------------------------------

#     assert result.get(
#         "errors",
#         []
#     ) == []

#     # -----------------------------------------
#     # WORKFLOW FINISHED
#     # -----------------------------------------

#     assert result.get(
#         "workflow_complete",
#         False
#     ) is True

#     # -----------------------------------------
#     # REPORT VALIDATION
#     # -----------------------------------------

#     report = result.get(
#         "report",
#         {}
#     )

#     if isinstance(report, dict):

#         assert report.get(
#             "title"
#         ) is not None

#         assert isinstance(
#             report.get(
#                 "references",
#                 []
#             ),
#             list
#         )
# =========================================================
# tests/integration/test_full_workflow.py
# =========================================================

from workflow.graph import (
    graph
)


def test_complete_workflow():

    initial_state = {

        # -----------------------------------------
        # SESSION
        # -----------------------------------------

        "thread_id":
            "test-thread",

        # -----------------------------------------
        # QUERY
        # -----------------------------------------

        "query":
            "Impact of AI on Healthcare",

        "subqueries":
            [],

        # -----------------------------------------
        # RETRIEVAL
        # -----------------------------------------

        "retrieved_docs":
            [],

        "vector_db":
            None,

        "routing":
            {
                "retrieval_mode":
                    "web_only"
            },

        "pdf_uploaded":
            False,

        # -----------------------------------------
        # ANALYSIS
        # -----------------------------------------

        "analysis":
            {},

        "validation":
            {},

        "report":
            {},

        "citations":
            [],

        # -----------------------------------------
        # HUMAN LOOP
        # -----------------------------------------

        "awaiting_human_approval":
            False,

        "human_feedback":
            "",

        # -----------------------------------------
        # EXECUTION
        # -----------------------------------------

        "errors":
            [],

        "retries":
            {},

        "workflow_complete":
            False,

        "critical_error":
            False,

        "next_agent":
            "supervisor",
    }

    result = graph.invoke(
        initial_state
    )

    # =====================================================
    # BASIC CHECKS
    # =====================================================

    assert result is not None

    assert isinstance(
        result,
        dict
    )

    # =====================================================
    # NO CRITICAL FAILURE
    # =====================================================

    assert not result.get(
        "critical_error",
        False
    )

    # =====================================================
    # ANALYSIS GENERATED
    # =====================================================

    assert "analysis" in result

    assert isinstance(
        result["analysis"],
        dict
    )

    # =====================================================
    # VALIDATION GENERATED
    # =====================================================

    assert "validation" in result

    # =====================================================
    # ERRORS SHOULD BE EMPTY
    # =====================================================

    assert result.get(
        "errors",
        []
    ) == []

    # =====================================================
    # HUMAN APPROVAL STATE
    # =====================================================

    assert result.get(
        "awaiting_human_approval",
        False
    ) is True

    # =====================================================
    # REPORT NOT GENERATED YET
    # =====================================================

    assert result.get(
        "report",
        {}
    ) == {}

    # =====================================================
    # WORKFLOW SHOULD PAUSE
    # =====================================================

    assert result.get(
        "workflow_complete",
        False
    ) is False