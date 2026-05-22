
from datetime import datetime

from prompts.analysis import (
    ANALYSIS_PROMPT
)
from rag.semantic_search import (
    semantic_search
)
from models.llm_registry import (
    reasoning_llm
)

from schemas.output import (
    AnalysisOutput
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

    vector_db = state.get(
        "vector_db"
    )

    retrieved_docs = []

    if vector_db:

        try:

            semantic_results = semantic_search(

                vector_db=vector_db,

                query=state["query"],

                k=15
            )

            for doc in semantic_results:

                retrieved_docs.append({

                    "title":
                        doc.metadata.get(
                            "title",
                            ""
                        ),

                    "content":
                        doc.page_content,

                    "url":
                        doc.metadata.get(
                            "url",
                            ""
                        ),

                    "source":
                        doc.metadata.get(
                            "source",
                            ""
                        ),

                    "page":
                        doc.metadata.get(
                            "page",
                            ""
                        )
                })

        except Exception as e:

            print(
                f"\nSemantic Retrieval Error: "
                f"{str(e)}"
            )

    # --------------------------------
    # DIRECT CONTEXT BUILD
    # --------------------------------

    context = "\n\n".join([

    f"""
SOURCE ID: {idx + 1}

TITLE:
{doc.get('title', 'No Title')}

URL:
{doc.get('url', 'No URL')}

CONTENT:
{doc.get('content', '')}
"""
    for idx, doc in enumerate(retrieved_docs)
])

    # print(
    #     f"\nContext Length: "
    #     f"{len(context)}"
    # )
    # print("Context")
    # print(context)

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
    # print("Final Analysis")
    # print(analysis)
    return {

        "analysis": analysis,

        "next_agent": "validator"
    }