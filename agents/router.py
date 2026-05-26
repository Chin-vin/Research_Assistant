from models.llm_registry import (
    fast_llm
)

from prompts.router import (
    ROUTER_PROMPT
)

from schemas.output import (
    RoutingOutput
)

structured_llm = (
    fast_llm.with_structured_output(
        RoutingOutput
    )
)


def retrieval_router_agent(state):

    query = state["query"]
    has_pdf = state.get("vector_db") is not None

    response = structured_llm.invoke(

        ROUTER_PROMPT.format(
            query=query,
             has_pdf=has_pdf
        )
    )

    routing = response.model_dump()
    
    print(
        f"Routing Mode: "
        f"{routing['retrieval_mode']}"
    )

    return {

        "routing": routing
    }