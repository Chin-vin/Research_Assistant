from models.llm_registry import (
    validator_llm
)

from prompts.validation import (
    VALIDATION_PROMPT
)

from schemas.output import (
    ValidationOutput
)


structured_llm = (
    validator_llm.with_structured_output(
        ValidationOutput
    )
)

MAX_RETRIES = 3


def validation_agent(state):

    # --------------------------------
    # ANALYSIS
    # --------------------------------

    analysis = state.get(
        "analysis",
        {}
    )

    # --------------------------------
    # VALIDATION PROMPT
    # --------------------------------

    prompt = VALIDATION_PROMPT.format(
        analysis=analysis
    )
    # --------------------------------
    # LLM VALIDATION
    # --------------------------------

    response = structured_llm.invoke(
        prompt
    )

    validation = response.model_dump()
    issues = validation.get(
    "issues",
    {}
)

    refinement = validation.get(
        "refinement",
        {}
    )

    print("\n========== VALIDATION ==========\n")

    print(
        f"Confidence Score: "
        f"{validation.get('confidence_score', 0.0)}"
    )

    print(
        f"Research Sufficient: "
        f"{validation.get('research_sufficient', False)}"
    )

    # --------------------------------
    # RETRY COUNT
    # --------------------------------

    retry_count = len(
        state.get(
            "errors",
            []
        )
    )

    # --------------------------------
    # STOP INFINITE RETRIES
    # --------------------------------

    if retry_count >= MAX_RETRIES:

        print(
            "\nMax retries reached."
        )

        return {

            "validation":
                validation,

            "next_agent":
                "reporter"
        }

    # --------------------------------
    # VALIDATION FLAGS
    # --------------------------------

    research_sufficient = validation.get(
        "research_sufficient",
        False
    )

    needs_refinement = refinement.get(
    "needs_refinement",
    False
)

    refinement_type = refinement.get(
    "refinement_type",
    ""
)

    refinement_focus = refinement.get(
    "refinement_focus",
    []
)

    
    # --------------------------------
    # SUCCESS CASE
    # --------------------------------

    if research_sufficient:

        return {

            "validation":
                validation,

            "next_agent":
                "human_approval"
        }

    # --------------------------------
    # BUILD FEEDBACK
    # --------------------------------

    feedback_parts = []

    feedback_for_retry = refinement.get(
    "feedback_for_retry",
    ""
)

    if feedback_for_retry:

        feedback_parts.append(
            feedback_for_retry
        )

    feedback_parts.extend(
        refinement_focus
    )

    weak_sections = issues.get(
    "weak_sections",
    []
)

    if weak_sections:

        feedback_parts.append(

            "Weak Sections: "
            + ", ".join(weak_sections)
        )

    missing_sections = issues.get(
    "missing_information",
    []
)

    if missing_sections:

        feedback_parts.append(

            "Missing Sections: "
            + ", ".join(missing_sections)
        )

    human_feedback = "\n".join(
        feedback_parts
    )

    # --------------------------------
    # UPDATE ERRORS
    # --------------------------------

    errors = state.get(
        "errors",
        []
    )

    errors.append(
        f"Validation refinement: "
        f"{refinement_type}"
    )

    # --------------------------------
    # RETRIEVAL REFINEMENT
    # --------------------------------

    if refinement_type == "retrieval":

        print(
            "\nValidator requested "
            "retrieval refinement."
        )

        return {

            "validation":
                validation,

            "human_feedback":
                human_feedback,

            "errors":
                errors,

            "next_agent":
                "parallel_retrieval"
        }

    # --------------------------------
    # ANALYSIS REFINEMENT
    # --------------------------------

    print(
        "\nValidator requested "
        "analysis refinement."
    )

    return {

        "validation":
            validation,

        "human_feedback":
            human_feedback,

        "errors":
            errors,

        "next_agent":
            "analyzer"
    }