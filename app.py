
from workflow.graph import (
    graph
)

from utils.pdf_generator import (
    generate_pdf_report
)

from rag.pdf_pipeline import (
    process_pdf
)

# --------------------------------
# USER QUERY
# --------------------------------

query = input(
    "Enter Research Query: "
)

# --------------------------------
# PDF INPUT
# --------------------------------

pdf_path_input = input(

    "Enter PDF Path "
    "(leave empty if none): "
).strip()

vector_db = None

# --------------------------------
# PROCESS PDF
# --------------------------------

if pdf_path_input:

    print(
        "\nProcessing Uploaded PDF..."
    )

    vector_db = process_pdf(
        pdf_path_input
    )

    print(
        "PDF Processed Successfully!"
    )

# --------------------------------
# INITIAL STATE
# --------------------------------

initial_state = {

    "query": query,

    "subqueries": [],

    "retrieved_docs": [],

    "analysis": {},

    "validation": {},

    "report": {},

    "citations": [],

    "errors": [],

    "workflow_complete": False,

    "next_agent": "supervisor",

    # ----------------------------
    # PDF RAG SUPPORT
    # ----------------------------

    "vector_db": vector_db,

    "pdf_uploaded":
        bool(pdf_path_input),

    # ----------------------------
    # DYNAMIC ROUTING
    # ----------------------------

    "routing": {}
}

# --------------------------------
# GRAPH EXECUTION
# --------------------------------

print(
    "\nRunning Multi-Agent Workflow..."
)

result = graph.invoke(

    initial_state,

    config={
        "recursion_limit": 15
    }
)

# --------------------------------
# REPORT
# --------------------------------

final_report = result.get(
    "report",
    {}
)

print("\nFINAL REPORT\n")

print(final_report)

# --------------------------------
# PDF GENERATION
# --------------------------------

pdf_path = generate_pdf_report(
    final_report
)

print(
    f"\nPDF Generated: {pdf_path}"
)

# --------------------------------
# ROUTING DEBUG
# --------------------------------

routing = result.get(
    "routing",
    {}
)

if routing:

    print(
        f"\nRetrieval Mode: "
        f"{routing.get('retrieval_mode')}"
    )