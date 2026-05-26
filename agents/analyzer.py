
from datetime import datetime

from prompts.analysis import (
    ANALYSIS_PROMPT
)
from rag.retriever import (
    retrieve_documents
)
from models.llm_registry import (
    reasoning_llm
)
import traceback

from schemas import state
from schemas.output import (
    AnalysisOutput
)
from utils.context_manager import (
    build_context
)
from rag.vectorstore import (
    load_vectorstore
)


structured_llm = (
    reasoning_llm.with_structured_output(
        AnalysisOutput
    )
)


def analysis_agent(state):
    print("Analyser agent")
    # --------------------------------
    # RETRIEVED DOCS
    # --------------------------------

    vector_db = load_vectorstore(
    state["thread_id"]
)

    retrieved_docs = []

    if vector_db:

        retrieved_docs = retrieve_documents(

            vector_db=vector_db,

            query=state["query"],

            k=15,

            rerank_top_k=8
        )

    # --------------------------------
    # DIRECT CONTEXT BUILD
    # --------------------------------
    context = build_context(
    retrieved_docs
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
    # ANALYSIS PROMPT
    # --------------------------------

    prompt = ANALYSIS_PROMPT.format(

    current_date=current_date,

    query=state["query"],

    validator_feedback=
        validator_feedback,

    documents=context,

    human_feedback=human_feedback
)
    
    

    # --------------------------------
    # LLM ANALYSIS
    # --------------------------------

    try:

        response = structured_llm.invoke(
            prompt
        )

        if response is None:
        
            raise Exception(
                "LLM returned empty response"
            )

        analysis = response.model_dump()
     
     

    except Exception as e:

        print("\n========== ANALYSIS ERROR ==========\n")

        print(str(e))

        raise Exception(
            f"Analysis generation failed: {str(e)}"
        )
    return {

        "analysis": analysis,
        # "vector_db":
        # state.get(
        #     "vector_db"
        # )
        # "next_agent": "validator"
    }