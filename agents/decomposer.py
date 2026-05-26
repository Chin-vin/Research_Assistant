

from prompts.decomposition import (
    DECOMPOSITION_PROMPT
)
from datetime import datetime
from models.llm_registry import (
    fast_llm
)

from schemas import state
from schemas.output import (
    DecompositionOutput
)

structured_llm = (
    fast_llm.with_structured_output(
        DecompositionOutput
    )
)


def decomposition_agent(state):

    # --------------------------------
    # QUERY
    # --------------------------------

    query = state.get(
        "query",
        ""
    )

    validator_feedback = state.get(
    "validator_feedback",
    ""
)

    human_feedback = state.get(
    "human_feedback",
    ""
)
    current_date = datetime.now().strftime(
    "%d-%m-%Y"
)
    # --------------------------------
    # PROMPT
    # --------------------------------

    prompt = DECOMPOSITION_PROMPT.format(

        query=query,

        validator_feedback=validator_feedback,
        human_feedback=human_feedback,
        current_date=current_date
    )

    # --------------------------------
    # LLM RESPONSE
    # --------------------------------

    response = structured_llm.invoke(
        prompt
    )

    result = response.model_dump()

    subqueries = result.get(
        "subqueries",
        []
    )

    # --------------------------------
    # CLEAN SUBQUERIES
    # --------------------------------

    cleaned_subqueries = []

    seen = set()

    for query in subqueries:

        query = query.strip()

        if not query:

            continue

        normalized = query.lower()

        if normalized in seen:

            continue

        seen.add(normalized)

        cleaned_subqueries.append(
            query
        )

    # --------------------------------
    # LIMIT OUTPUT
    # --------------------------------

    cleaned_subqueries = (
        cleaned_subqueries[:6]
    )
   
    print(
        f"\nGenerated Subqueries: "
        f"{len(cleaned_subqueries)}"
    )

    for idx, subquery in enumerate(
        cleaned_subqueries
    ):

        print(
            f"{idx + 1}. {subquery}"
        )

    # --------------------------------
    # RETURN
    # --------------------------------

    return {

        "subqueries":
            cleaned_subqueries,

        # "next_agent":
        #     "parallel_retrieval"
    }
