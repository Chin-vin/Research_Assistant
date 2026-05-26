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

    try:

        query = state["query"]

        has_pdf = (
            state.get("vector_db")
            is not None
        )

        response = structured_llm.invoke(

            ROUTER_PROMPT.format(

                query=query,

                has_pdf=has_pdf
            )
        )

        if response is None:

            raise ValueError(
                "Router returned empty response"
            )

        routing = response.model_dump()

        print(
            f"Routing Mode: "
            f"{routing['retrieval_mode']}"
        )

        return {

            "routing": routing
        }

    except Exception as e:

        print(
            "\n========== ROUTER ERROR ==========\n"
        )

        print(str(e))

        # IMPORTANT:
        # preserve original exception type
        raise