
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

from groq import (
    RateLimitError,
    APITimeoutError,
    APIConnectionError,
    BadRequestError
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

    section_operation = state.get(
        "section_operation",
        {}
    )

    operation = section_operation.get(
        "operation",
        "none"
    )

    target_section = section_operation.get(
        "target_section",
        ""
    ).strip().lower()

    if operation == "update":

        query_text = target_section

        section_instruction = f'''

Generate ONLY UPDATED VERSION
of this section:

{target_section}

Preserve unrelated sections.

'''

    else:

        query_text = state["query"]

        section_instruction = ""

    current_date = datetime.now().strftime(
    "%d-%m-%Y"
)
    
    # --------------------------------
    # ANALYSIS PROMPT
    # --------------------------------

    previous_analysis = state.get(
    "previous_analysis",
    {}
) or {}

    previous_sections = previous_analysis.get(
        "dynamic_sections",
        []
    )

    existing_sections = ""

    for section in previous_sections:

        existing_sections += f"""

SECTION:
{section.get("heading", "")}

CONTENT:
{section.get("content", "")}

"""

    prompt = ANALYSIS_PROMPT.format(

    current_date=current_date,

    query=query_text,

    validator_feedback=
        validator_feedback,

    documents=context,

    human_feedback=human_feedback,

    existing_sections=existing_sections,

    section_operation=section_operation,

    section_instruction=section_instruction
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

        if operation == "update":

            new_sections = analysis.get(
                "dynamic_sections",
                []
            )

            updated_sections = []

            for old_section in previous_sections:

                old_heading = old_section.get(
                    "heading",
                    ""
                ).strip().lower()

                replaced = False

                for new_section in new_sections:

                    new_heading = new_section.get(
                        "heading",
                        ""
                    ).strip().lower()

                    if (
                        target_section == old_heading
                        or target_section == new_heading
                        or old_heading in target_section
                        or target_section in old_heading
                    ):

                        updated_sections.append(
                            new_section
                        )

                        replaced = True
                        break

                if not replaced:

                    updated_sections.append(
                        old_section
                    )

            previous_analysis[
                "dynamic_sections"
            ] = updated_sections

            analysis = previous_analysis

        else:

            merged_sections = {}

            for section in previous_sections:

                heading = section.get(
                    "heading",
                    ""
                ).strip()

                if heading:

                    merged_sections[
                        heading.lower()
                    ] = section

            for section in analysis.get(
                "dynamic_sections",
                []
            ):

                heading = section.get(
                    "heading",
                    ""
                ).strip()

                if heading:

                    merged_sections[
                        heading.lower()
                    ] = section

            analysis["dynamic_sections"] = list(
                merged_sections.values()
            )
             
     

    except Exception as e:

        traceback.print_exc()

        # =====================================
        # ERROR TYPE DETECTION
        # =====================================

        if isinstance(
            e,
            RateLimitError
        ):

            error_title = (
                "Rate Limit Exceeded"
            )

        elif isinstance(
            e,
            APITimeoutError
        ):

            error_title = (
                "Request Timeout"
            )

        elif isinstance(
            e,
            APIConnectionError
        ):

            error_title = (
                "API Connection Error"
            )

        elif isinstance(
            e,
            BadRequestError
        ):

            error_title = (
                "Bad Request Error"
            )

        elif isinstance(
            e,
            json.JSONDecodeError
        ):

            error_title = (
                "JSON Parsing Failed"
            )

        elif isinstance(
            e,
            ValueError
        ):

            error_title = (
                "Validation Error"
            )

        else:

            error_title = type(e).__name__

        return {

            "critical_error": True,

            "workflow_complete": True,

            "next_agent": "FINISH",

            "error": {

                "type": error_title,

                "message": str(e),

                "raw": traceback.format_exc()
            }
        }


    return {

        "analysis": analysis,
        # "vector_db":
        # state.get(
        #     "vector_db"
        # )
        # "next_agent": "validator"
    }