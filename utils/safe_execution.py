import time
import traceback

from json import (
    JSONDecodeError
)
from utils.retry import retry_with_backoff
from pydantic import (
    ValidationError
)

from requests.exceptions import (
    Timeout
)

from utils.logger import logger


# =========================================================
# SAFE OPTIONAL IMPORT
# =========================================================

try:

    from groq import (
        RateLimitError
    )

except Exception:

    class RateLimitError(Exception):

        pass


# =========================================================
# CONFIG
# =========================================================

MAX_RETRIES = 2


# =========================================================
# AGENT MAP
# =========================================================

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


# =========================================================
# SAFE EXECUTION
# =========================================================

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

        # =====================================================
        # OUTPUT VALIDATION
        # =====================================================

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

    # =========================================================
    # HANDLE FAILURES
    # =========================================================

    except Exception as e:

        traceback.print_exc()

        raw_error = traceback.format_exc()

        logger.error(raw_error)

        error_message = str(e)

        error_type = type(e).__name__

        # =====================================================
        # ERROR STORAGE
        # =====================================================

        errors = state.get(
            "errors",
            []
        )

        errors.append(
            error_message
        )

        # =====================================================
        # ERROR TYPES
        # =====================================================

        fatal_errors = (

            ValidationError,

            JSONDecodeError,

            RecursionError
        )

        retryable_errors = (

            RateLimitError,

            Timeout
        )

        # =====================================================
        # FATAL ERRORS
        # =====================================================

        if isinstance(
            e,
            fatal_errors
        ):

            logger.error(
                f"Fatal Error: {error_type}"
            )

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
                    error_type,

                "next_agent":
                    "FINISH"
            }

        # =====================================================
        # RETRIES
        # =====================================================

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

        current_retry = retries[
            agent_function.__name__
        ]

        logger.warning(

            f"{agent_function.__name__} "
            f"failed | Retry: "
            f"{current_retry}"
        )

        # =====================================================
        # MAX RETRIES
        # =====================================================

        if current_retry >= MAX_RETRIES:

            logger.error(
                f"Max retries reached for "
                f"{agent_function.__name__}"
            )

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
                    error_type,

                "next_agent":
                    "FINISH"
            }

        # =====================================================
        # RETRYABLE ERRORS
        # =====================================================

        if isinstance(
            e,
            retryable_errors
        ):

            # ================================================
            # EXPONENTIAL BACKOFF
            # ================================================

            result = retry_with_backoff(

    lambda: agent_function(
        state
    ),

    retries=MAX_RETRIES
)


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

        # =====================================================
        # UNKNOWN ERRORS
        # =====================================================

        logger.error(
            f"Unhandled Error: {error_type}"
        )

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
                error_type,

            "next_agent":
                "FINISH"
        }