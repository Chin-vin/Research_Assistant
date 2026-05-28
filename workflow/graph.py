from langgraph.graph import (
    StateGraph,
    END
)

from schemas.state import (
    AgentState
)

# -----------------------------------
# AGENTS
# -----------------------------------

from agents.supervisor import (
    supervisor_agent
)

from agents.decomposer import (
    decomposition_agent
)

from agents.router import (
    retrieval_router_agent
)

from agents.web_retriever import (
    web_retriever_agent
)

from agents.pdf_retriever import (
    pdf_retriever_agent
)

from agents.arxiv_retriever import (
    arxiv_retriever_agent
)

from agents.analyzer import (
    analysis_agent
)

from agents.add_section_agent import (
    add_section_agent
)

from agents.validator import (
    validation_agent
)

from agents.reporter import (
    reporting_agent
)


from agents.human_approval import (
    human_approval_agent
)

from agents.human_intent_router import (
    human_intent_router_agent
)
# -----------------------------------
# SAFE EXECUTION
# -----------------------------------

from utils.safe_execution import (
    safe_execute
)

# -----------------------------------
# GRAPH BUILDER
# -----------------------------------

builder = StateGraph(
    AgentState
)

# -----------------------------------
# NODES
# -----------------------------------

builder.add_node(
    "supervisor",
    supervisor_agent
)

builder.add_node(
    "decomposer",
    lambda state:
        safe_execute(
            decomposition_agent,
            state
        )
)

builder.add_node(
    "router",
    lambda state:
        safe_execute(
            retrieval_router_agent,
            state
        )
)

builder.add_node(
    "web_retriever",
    lambda state:
        safe_execute(
            web_retriever_agent,
            state
        )
)

builder.add_node(
    "pdf_retriever",
    lambda state:
        safe_execute(
            pdf_retriever_agent,
            state
        )
)

builder.add_node(
    "arxiv_retriever",
    lambda state:
        safe_execute(
            arxiv_retriever_agent,
            state
        )
)

builder.add_node(
    "analyzer",
    lambda state:
        safe_execute(
            analysis_agent,
            state
        )
)

builder.add_node(
    "add_section_agent",
    lambda state:
        safe_execute(
            add_section_agent,
            state
        )
)

builder.add_node(
    "validator",
    lambda state:
        safe_execute(
            validation_agent,
            state
        )
)

builder.add_node(
    "reporter",
    lambda state:
        safe_execute(
            reporting_agent,
            state
        )
)

builder.add_node(

    "human_approval",

    lambda state:
        safe_execute(
            human_approval_agent,
            state
        )
)
builder.add_node(

    "human_intent_router",

    lambda state:
        safe_execute(
            human_intent_router_agent,
            state
        )
)

# -----------------------------------
# ENTRY POINT
# -----------------------------------

builder.set_entry_point(
    "supervisor"
)


# -----------------------------------
# SUPERVISOR ROUTING
# -----------------------------------

builder.add_conditional_edges(

    "supervisor",
    lambda state:

(

    state.get(
        "next_agent",
        "FINISH"
    )

    if state.get(
        "next_agent"
    ) in {

        "decomposer",

        "router",

        "web_retriever",

        "pdf_retriever",

        "arxiv_retriever",

        "analyzer",

        "validator",

        "reporter",

        "human_approval",

        "human_intent_router",

        "FINISH"
    }

    else "FINISH"
),

    {

        "decomposer":
            "decomposer",

        "router":
            "router",
        

        "human_approval":
            "human_approval",
        
    "human_intent_router":
        "human_intent_router",

        "analyzer":
            "analyzer",

        "validator":
            "validator",

        "reporter":
            "reporter",

        "FINISH":
            END
    }
)
builder.add_conditional_edges(

    "human_intent_router",

    lambda state:

(

    state.get(
        "next_agent",
        "FINISH"
    )

    if state.get(
        "next_agent"
    ) in {

        "decomposer",

        "router",

        "pdf_retriever",

        "analyzer",

        "validator",

        "reporter",

        "FINISH"
    }

    else "FINISH"
),

    {

        "decomposer":
            "decomposer",

        "router":
            "router",

        "pdf_retriever":
            "pdf_retriever",

        "analyzer":
            "analyzer",

        "validator":
            "validator",

        "reporter":
            "reporter",
        
        "FINISH":
        END
    }
)
# -----------------------------------
# MAIN WORKFLOW
# -----------------------------------

builder.add_edge(
    "decomposer",
    "router"
)

# -----------------------------------
# RETRIEVAL FLOW
# -----------------------------------

builder.add_edge(
    "router",
    "web_retriever"
)

builder.add_edge(
    "web_retriever",
    "pdf_retriever"
)

# builder.add_edge(
#     "pdf_retriever",
#     "arxiv_retriever"
# )

# builder.add_edge(
#     "arxiv_retriever",
#     "analyzer"
# )

builder.add_conditional_edges(
    "pdf_retriever",
    lambda state:
        "add_section_agent"
        if state.get(
            "section_operation",
            {}
        ).get(
            "operation",
            "none"
        ) == "add"
        else "analyzer",
    {
        "add_section_agent":
            "add_section_agent",
        "analyzer":
            "analyzer"
    }
)
# -----------------------------------
# ANALYSIS FLOW
# -----------------------------------

builder.add_edge(
    "analyzer",
    "validator"
)

builder.add_edge(
    "add_section_agent",
    "validator"
)
builder.add_conditional_edges(

    "validator",

    lambda state:

(

    state.get(
        "next_agent",
        "human_approval"
    )

    if state.get(
        "next_agent"
    ) in {

        "human_approval",

        "analyzer",

        "reporter",

        "FINISH"
    }

    else "FINISH"
),

    {

        "human_approval":
            "human_approval",
        "analyzer":
            "analyzer",

        "reporter":
            "reporter",

        "FINISH":
            END
    }
)
# builder.add_edge(
#     "validator",
#     "human_approval"
# )

builder.add_conditional_edges(

    "human_approval",
    lambda state:

(

    state.get(
        "next_agent",
        "FINISH"
    )

    if state.get(
        "next_agent"
    ) in {

        "reporter",

        "analyzer",

        "human_intent_router",

        "HUMAN_INPUT",

        "FINISH"
    }

    else "FINISH"
),

    {

        "reporter":
            "reporter",

        "analyzer":
            "analyzer",

        "human_intent_router":
            "human_intent_router",

        "HUMAN_INPUT":
            END,

        "FINISH":
            END
    }
)
builder.add_conditional_edges(

    "reporter",

    lambda state:

        "FINISH"

        if state.get(
            "critical_error",
            False
        )

        else "SUCCESS",

    {

        "SUCCESS":
            END,

        "FINISH":
            END
    }
)
# -----------------------------------
# COMPILE GRAPH
# -----------------------------------

graph = builder.compile()
