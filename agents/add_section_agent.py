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


def add_section_agent(state):

    previous_analysis = state.get(
        "analysis",
        {}
    )

    previous_sections = previous_analysis.get(
        "dynamic_sections",
        []
    )

    section_operation = state.get(
        "section_operation",
        {}
    )

    target_section = section_operation.get(
        "target_section",
        ""
    )

    vector_db = load_vectorstore(
        state["thread_id"]
    )

    retrieved_docs = []

    if vector_db:

        retrieved_docs = retrieve_documents(

            vector_db=vector_db,

            query=target_section,

            k=15,

            rerank_top_k=8
        )

    context = build_context(
        retrieved_docs
    )

    current_date = datetime.now().strftime(
        "%d-%m-%Y"
    )

    existing_sections = ""

    for section in previous_sections:

        existing_sections += f'''

SECTION:
{section.get("heading", "")}

CONTENT:
{section.get("content", "")}

'''

    prompt = ANALYSIS_PROMPT.format(

        current_date=current_date,

        query=target_section,

        validator_feedback="",

        documents=context,

        human_feedback=state.get(
            "human_feedback",
            ""
        ),

        existing_sections=existing_sections,

        section_operation=section_operation,

        section_instruction=f'''

Generate ONLY ONE NEW SECTION.

TARGET SECTION:
{target_section}

Do NOT regenerate old sections.

'''
    )

    response = structured_llm.invoke(
        prompt
    )

    analysis = response.model_dump()

    new_sections = analysis.get(
        "dynamic_sections",
        []
    )

    final_sections = previous_sections.copy()

    for new_section in new_sections:

        final_sections.append(
            new_section
        )

    final_analysis = previous_analysis.copy()
    final_analysis[
        "dynamic_sections"
    ] = final_sections

    return {

        "analysis":
            final_analysis
    }