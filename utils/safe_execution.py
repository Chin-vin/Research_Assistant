import time
import traceback

from json import (
    JSONDecodeError
)
from schemas import state
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

def build_error_response(

    state,

    error_type,

    error_message,

    raw_error=None
):

    errors = state.get(
        "errors",
        []
    )

    errors.append(
        error_message
    )

    return {

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

        "error": {

            "type":
                error_type,

            "message":
                error_message,

            "raw":
                raw_error
        },

        "errors":
            errors,

        "next_agent":
            "FINISH"
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
            
        retries = state.get(
            "retries",
            {}
        )

        if agent_function.__name__ in retries:
        
            retries[
                agent_function.__name__
            ] = 0

        state["retries"] = retries
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
        print("\n" + "=" * 80) 
        print("SAFE EXECUTE CAUGHT ERROR") 
        print("=" * 80) 
        print("AGENT:") 
        print(agent_function.__name__) 
        print("\nERROR TYPE:") 
        print(error_type) 
        print("\nERROR MESSAGE:") 
        print(error_message) 
        print("\nRETRIES:") 
        print(state.get("retries")) 
        print("=" * 80 + "\n")

        
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

            return build_error_response(

    state=state,

    error_type=error_type,

    error_message=error_message,

    raw_error=raw_error
)

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
        state["retries"] = retries
        logger.warning(

            f"{agent_function.__name__} "
            f"failed | Retry: "
            f"{current_retry}"
        )

        

        # =====================================================
        # RETRYABLE ERRORS
        # =====================================================

        combined_error = error_message.lower()

        # =========================================
        # NON-RETRYABLE QUOTA EXHAUSTION
        # =========================================

        quota_exhausted = (
        
            "tokens per day" in combined_error

            or "tpd" in combined_error

            or "quota exceeded" in combined_error

            or "insufficient quota"
                in combined_error
        )

        # =========================================
        # TEMPORARY RETRYABLE LIMITS
        # =========================================

        temporary_rate_limit = (

    isinstance(
        e,
        retryable_errors
    )

    or "429" in combined_error

    or "rate limit"
        in combined_error

    or "too many requests"
        in combined_error

    or "resource exhausted"
        in combined_error

    or "quota" in combined_error

    or "tokens per minute"
        in combined_error

    or "requests per minute"
        in combined_error

    or "service unavailable"
        in combined_error
)

        is_retryable = (
        
            temporary_rate_limit

            and not quota_exhausted
        )

        # =========================================
        # DAILY QUOTA EXHAUSTED
        # =========================================

        if quota_exhausted:
        
            logger.error(
                "Daily token quota exhausted"
            )

            return build_error_response(
            
                state=state,

                error_type=
                    "RateLimitError",

                error_message=
                    "Daily token quota exhausted",

                raw_error=
                    raw_error
            )

        # =========================================
        # RETRY TEMPORARY FAILURES
        # =========================================

        if is_retryable:
        
            if current_retry >= MAX_RETRIES:
            
                logger.error(
                
                    f"Max retries reached for "
                    f"{agent_function.__name__}"
                )

                return build_error_response(
                
                    state=state,

                    error_type=error_type,

                    error_message=error_message,

                    raw_error=raw_error
                )

            print(

                f"\nTrying again... "
                f"Attempt "
                f"{current_retry}/"
                f"{MAX_RETRIES}"
            )
            
            time.sleep(5)
            
            return safe_execute(
                agent_function,
                state
            )
            

        # =====================================================
        # UNKNOWN ERRORS
        # =====================================================

        logger.error(
            f"Unhandled Error: {error_type}"
        )

        return build_error_response(

    state=state,

    error_type=error_type,

    error_message=error_message,

    raw_error=raw_error
)