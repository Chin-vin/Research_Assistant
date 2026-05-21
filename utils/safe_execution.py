import traceback

from utils.logger import logger

MAX_RETRIES = 3


def safe_execute(agent_function, state):

    try:

        logger.info(f"Running {agent_function.__name__}")

        return agent_function(state)

    except Exception as e:

        traceback.print_exc()

        logger.error(str(e))

        errors = state.get("errors", [])
        errors.append(str(e))

        retries = state.get("retries", {})

        retries[agent_function.__name__] = (
            retries.get(agent_function.__name__, 0) + 1
        )

        if retries[agent_function.__name__] >= MAX_RETRIES:

            return {
                "errors": errors,
                "workflow_complete": True,
                "next_agent": "fallback"
            }

        return {
            "errors": errors,
            "retries": retries,
            "next_agent": agent_function.__name__
        }