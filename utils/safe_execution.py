import traceback

from utils.logger import logger

MAX_RETRIES = 3


AGENT_NAME_MAP = {

    "decomposition_agent":
        "decomposer",

    "retrieval_router_agent":
        "router",

    "web_retriever_agent":
        "web_retriever",

    "pdf_retriever_agent":
        "pdf_retriever",

    "arxiv_retriever_agent":
        "arxiv_retriever",

    "analysis_agent":
        "analyzer",

    "validation_agent":
        "validator",

    "reporting_agent":
        "reporter",

    "human_approval_agent":
        "human_approval",

    "human_intent_router_agent":
        "human_intent_router"
}


def safe_execute(

    agent_function,

    state
):

    try:

        logger.info(
            f"Running {agent_function.__name__}"
        )

        result = agent_function(
            state
        )

        # =========================================
        # VALIDATION
        # =========================================

        if result is None:

            raise Exception(
                "Agent returned None"
            )

        if not isinstance(
            result,
            dict
        ):

            raise Exception(
                "Agent returned invalid format"
            )

        return result

    except Exception as e:

        traceback.print_exc()

        raw_error = traceback.format_exc()

        error_message = str(e)

        logger.error(raw_error)

        errors = state.get(
            "errors",
            []
        )

        errors.append(error_message)

        error_lower = (
            error_message.lower()
        )

        # =========================================
        # RATE LIMIT DETECTION
        # =========================================

        rate_limit_error = any([

            "rate limit" in error_lower,

            "429" in error_lower,

            "quota" in error_lower,

            "too many requests" in error_lower,

            "resource exhausted" in error_lower,

            "ratelimiterror" in error_lower,

            "tokens per minute" in error_lower,

            "requests per day" in error_lower,

            "capacity" in error_lower,

            "model overloaded" in error_lower,

            "daily limit" in error_lower,

            "groqerror" in error_lower
        ])

        timeout_error = any([

            "timeout" in error_lower,

            "timed out" in error_lower
        ])

        schema_error = any([

            "validationerror"
            in error_lower,

            "schema" in error_lower,

            "json" in error_lower
        ])

        recursion_error = any([

            "recursion" in error_lower
        ])

        # =========================================
        # CRITICAL ERRORS
        # =========================================

        if any([

            rate_limit_error,

            timeout_error,

            schema_error,

            recursion_error
        ]):

            return {

                "errors":
                    errors,

                "workflow_complete":
                    True,

                "critical_error":
                    True,

                "awaiting_human_approval":
                    False,

                "workflow_running":
                    False,

                "report":
                    None,

                "error_type":

                    "RATE_LIMIT"

                    if rate_limit_error

                    else "WORKFLOW_ERROR",

                "next_agent":
                    "FINISH"
            }

        # =========================================
        # RETRY LOGIC
        # =========================================

        retries = state.get(
            "retries",
            {}
        )

        retries[
            agent_function.__name__
        ] = (

            retries.get(
                agent_function.__name__,
                0
            ) + 1
        )

        # =========================================
        # MAX RETRIES
        # =========================================

        if retries[
            agent_function.__name__
        ] >= MAX_RETRIES:

            return {

                "errors":
                    errors,

                "workflow_complete":
                    True,

                "critical_error":
                    True,

                "awaiting_human_approval":
                    False,

                "workflow_running":
                    False,

                "report":
                    None,

                "error_type":
                    "WORKFLOW_ERROR",

                "next_agent":
                    "FINISH"
            }

        # =========================================
        # SAFE RETRY
        # =========================================

        return {

            "errors":
                errors,

            "retries":
                retries,

            "next_agent":
                AGENT_NAME_MAP.get(
                    agent_function.__name__,
                    "FINISH"
                )
        }
# # import traceback

# # from utils.logger import logger

# # MAX_RETRIES = 3


# # def safe_execute(agent_function, state):

# #     try:

# #         logger.info(f"Running {agent_function.__name__}")

# #         return agent_function(state)
    
# #     except Exception as e:

# #         traceback.print_exc()

# #         error_message = str(e)

# #         logger.error(error_message)

# #         errors = state.get(
# #             "errors",
# #             []
# #         )

# #         errors.append(error_message)

# #         # =====================================================
# #         # RATE LIMIT DETECTION
# #         # =====================================================

# #         rate_limit_detected = any([

# #             "rate limit" in error_message.lower(),

# #             "429" in error_message,

# #             "quota" in error_message.lower(),

# #             "too many requests" in error_message.lower(),

# #             "resource exhausted" in error_message.lower()
# #         ])

# #         # =====================================================
# #         # STOP IMMEDIATELY ON RATE LIMIT
# #         # =====================================================

# #         if rate_limit_detected:

# #             return {

# #                 "errors": errors,

# #                 "workflow_complete": True,

# #                 "rate_limit_error": True,

# #                 "next_agent": "FINISH"
# #             }

# #         # =====================================================
# #         # NORMAL RETRIES
# #         # =====================================================

# #         retries = state.get(
# #             "retries",
# #             {}
# #         )

# #         retries[
# #             agent_function.__name__
# #         ] = (

# #             retries.get(
# #                 agent_function.__name__,
# #                 0
# #             ) + 1
# #         )

# #         # =====================================================
# #         # MAX RETRIES REACHED
# #         # =====================================================

# #         if retries[
# #             agent_function.__name__
# #         ] >= MAX_RETRIES:

# #             return {

# #                 "errors": errors,

# #                 "workflow_complete": True,

# #                 "next_agent": "FINISH"
# #             }

# #         # =====================================================
# #         # RETRY SAME AGENT
# #         # =====================================================

# #         return {

# #             "errors": errors,

# #             "retries": retries,

# #             "next_agent":
# #                 agent_function.__name__
# #         }

# #     # except Exception as e:

# #     #     traceback.print_exc()

# #     #     logger.error(str(e))

# #     #     errors = state.get("errors", [])
# #     #     errors.append(str(e))

# #     #     retries = state.get("retries", {})

# #     #     retries[agent_function.__name__] = (
# #     #         retries.get(agent_function.__name__, 0) + 1
# #     #     )

# #     #     if retries[agent_function.__name__] >= MAX_RETRIES:

# #     #         return {
# #     #             "errors": errors,
# #     #             "workflow_complete": True,
# #     #             "next_agent": "fallback"
# #     #         }

# #     #     return {
# #     #         "errors": errors,
# #     #         "retries": retries,
# #     #         "next_agent": agent_function.__name__
# #     #     }
# import traceback

# from utils.logger import logger


# MAX_RETRIES = 3


# def safe_execute(

#     agent_function,

#     state
# ):

#     try:

#         logger.info(
#             f"Running {agent_function.__name__}"
#         )

#         result = agent_function(
#             state
#         )

#         # =====================================================
#         # EMPTY RESULT PROTECTION
#         # =====================================================

#         if result is None:

#             raise Exception(
#                 "Agent returned None"
#             )

#         if not isinstance(
#             result,
#             dict
#         ):

#             raise Exception(
#                 "Agent returned invalid format"
#             )

#         return result

#     # =========================================================
#     # HANDLE ALL FAILURES
#     # =========================================================

#     except Exception as e:

#         traceback.print_exc()

#         error_message = str(e)

#         logger.error(error_message)

#         errors = state.get(
#             "errors",
#             []
#         )

#         errors.append(error_message)

#         # =====================================================
#         # ERROR TYPE DETECTION
#         # =====================================================

#         error_lower = (
#             error_message.lower()
#         )

#         rate_limit_error = any([

#     "rate limit" in error_lower,

#     "429" in error_lower,

#     "quota" in error_lower,

#     "too many requests" in error_lower,

#     "resource exhausted" in error_lower,

#     "ratelimiterror" in error_lower,

#     "tokens per minute" in error_lower,

#     "requests per day" in error_lower,

#     "capacity" in error_lower,

#     "model overloaded" in error_lower,

#     "daily limit" in error_lower,

#     "groqerror" in error_lower
# ])

#         timeout_error = any([

#             "timeout" in error_lower,

#             "timed out" in error_lower
#         ])

#         schema_error = any([

#             "validationerror"
#             in error_lower,

#             "schema" in error_lower,

#             "json" in error_lower
#         ])

#         recursion_error = any([

#             "recursion" in error_lower
#         ])

#         # =====================================================
#         # CRITICAL FAILURES
#         # =====================================================

#         if any([

#             rate_limit_error,

#             timeout_error,

#             schema_error,

#             recursion_error
#         ]):

#             return {

#                 "errors":
#                     errors,

#                 "workflow_complete":
#                     True,

#                 "critical_error":
#                     True,

#                 "error_type":
#                     error_message,

#                 "next_agent":
#                     "FINISH"
#             }

#         # =====================================================
#         # RETRY LOGIC
#         # =====================================================

#         retries = state.get(
#             "retries",
#             {}
#         )

#         retries[
#             agent_function.__name__
#         ] = (

#             retries.get(
#                 agent_function.__name__,
#                 0
#             ) + 1
#         )

#         # =====================================================
#         # MAX RETRIES
#         # =====================================================

#         if retries[
#             agent_function.__name__
#         ] >= MAX_RETRIES:

#             return {

#                 "errors":
#                     errors,

#                 "workflow_complete":
#                     True,

#                 "critical_error":
#                     True,

#                 "error_type":
#                     error_message,

#                 "next_agent":
#                     "FINISH"
#             }

#         # =====================================================
#         # SAFE RETRY
#         # =====================================================

#         AGENT_NAME_MAP = {

#         "decomposition_agent":
#             "decomposer",

#         "retrieval_router_agent":
#             "router",

#         "web_retriever_agent":
#             "web_retriever",

#         "pdf_retriever_agent":
#             "pdf_retriever",

#         "arxiv_retriever_agent":
#             "arxiv_retriever",

#         "analysis_agent":
#             "analyzer",

#         "validation_agent":
#             "validator",

#         "reporting_agent":
#             "reporter",

#         "human_approval_agent":
#             "human_approval",

#         "human_intent_router_agent":
#             "human_intent_router"
#     }

#     return {

#         "errors":
#             errors,

#         "retries":
#             retries,

#         "next_agent":
#             AGENT_NAME_MAP.get(
#                 agent_function.__name__,
#                 "FINISH"
#             )
#     }