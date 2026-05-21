def human_approval_agent(state):

    analysis = state.get(
        "analysis",
        {}
    )

    validation = state.get(
        "validation",
        {}
    )

    print(
        "\nWaiting For Human Approval..."
    )
    

    return {

        "analysis":
            analysis,

        "validation":
            validation,

        "awaiting_human_approval":
            True,

        "next_agent":
            "HUMAN_INPUT"
    }