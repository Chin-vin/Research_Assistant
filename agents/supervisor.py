
def supervisor_agent(state):
    if state.get("next_agent") == "human_intent_router":

        return {
            "next_agent":
                "human_intent_router"
        }

    if state.get("next_agent") == "reporter":

        return {
            "next_agent":
                "reporter"
        }


    if not state.get("subqueries"):

        return {
            "next_agent": "decomposer"
        }

    if not state.get("retrieved_docs"):

        return {
            "next_agent": "parallel_retrieval"
        }

    if not state.get("analysis"):

        return {
            "next_agent": "analyzer"
        }

    if not state.get("validation"):

        return {
            "next_agent": "validator"
        }

    if not state["validation"].get(
        "research_sufficient"
    ):

        return {
            "next_agent": "parallel_retrieval"
        }

    return {
        "next_agent": "reporter"
    }