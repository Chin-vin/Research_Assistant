from datetime import (
    datetime
)

from models.llm_registry import (
    report_llm
)

from prompts.reporting import (
    REPORT_PROMPT
)

from schemas.output import (
    ReportOutput
)



structured_llm = (
    report_llm.with_structured_output(
        ReportOutput
    )
)


def reporting_agent(state):
    print("Rport agent")
    # --------------------------------
    # ANALYSIS
    # --------------------------------

    analysis = state.get(
        "analysis",
        {}
    )

    # --------------------------------
    # SAFE FIELD EXTRACTION
    # --------------------------------

    findings = analysis.get(
        "key_findings",
        []
    )

    # --------------------------------
    # DYNAMIC SECTIONS
    # --------------------------------
    dynamic_sections = analysis.get(
    "dynamic_sections",
    []
)
    citations=[]
    for section in dynamic_sections:

        section_citations = section.get(
            "citations",
            []
        )

        for citation in section_citations:

            if citation not in citations:

                citations.append(citation)
    # --------------------------------
    # CURRENT DATE
    # --------------------------------

    current_date = datetime.now().strftime(
        "%d-%m-%Y"
    )

    # --------------------------------
    # QUERY
    # --------------------------------

    query = state.get(
        "query",
        ""
    )

    human_feedback = state.get(
    "human_feedback",
    ""
)
    # --------------------------------
    # PROMPT
    # --------------------------------

    prompt = REPORT_PROMPT.format(

    current_date=current_date,

    query=query,

    findings=findings,

    dynamic_sections=dynamic_sections,

    citations=citations,

    human_feedback=human_feedback
)


    print(
        f"\nCitations Count: "
        f"{len(citations)}"
    )
    
    # --------------------------------
    # GENERATE REPORT
    # --------------------------------

    try:

        response = structured_llm.invoke(
            prompt
        )

        report = response.model_dump()

    except Exception as e:
        
        print(
            f"\nReport Generation Error: {e}"
        )
    
        return {
        
            "critical_error": True,
    
            "errors": [
                str(e)
            ],
    
            "workflow_complete": True,
    
            "next_agent": "FINISH"
        }

    # --------------------------------
    # RETURN
    # --------------------------------

    return {

        "report": report,

        "workflow_complete": True,

        "next_agent": "FINISH"
    }