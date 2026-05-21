from prompts.human_router import (
    HUMAN_ROUTER_PROMPT
)

from models.llm_registry import (
    fast_llm
)

from schemas.output import (
    HumanIntentOutput
)


structured_llm = (

    fast_llm.with_structured_output(
        HumanIntentOutput
    )
)


def human_intent_router_agent(state):

    feedback = state.get(
        "human_feedback",
        ""
    )

    prompt = HUMAN_ROUTER_PROMPT.format(

        feedback=feedback
    )

    response = structured_llm.invoke(
        prompt
    )

    result = response.model_dump()

    target_agent = result.get(
    "target_agent",
    "analyzer"
)

    print(
    f"\nHuman Intent Routing → "
    f"{target_agent}"
)

    return {

    "next_agent":
        target_agent
}