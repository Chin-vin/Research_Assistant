# from models.llm_registry import (
#     validator_llm
# )

# from prompts.validation import (
#     VALIDATION_PROMPT
# )

# from schemas.output import (
#     ValidationOutput
# )

# structured_llm = (
#     validator_llm.with_structured_output(
#         ValidationOutput
#     )
# )

# MAX_RETRIES = 5


# def validation_agent(state):
#     # --------------------------------
#     # ANALYSIS
#     # --------------------------------

#     analysis = state.get(
#         "analysis",
#         {}
#     )

#     # --------------------------------
#     # VALIDATION PROMPT
#     # --------------------------------

#     prompt = VALIDATION_PROMPT.format(
#         analysis=analysis
#     )
#     # --------------------------------
#     # LLM VALIDATION
#     # --------------------------------

#     response = structured_llm.invoke(
#         prompt
#     )

#     validation = response.model_dump()

#     issues = validation.get(
#         "issues",
#         {}
#     )

#     refinement = validation.get(
#         "refinement",
#         {}
#     )

#     weak_sections = issues.get(
#         "weak_sections",
#         []
#     )

#     missing_sections = issues.get(
#         "missing_information",
#         []
#     )
    
#     print("\n========== VALIDATION ==========\n")

#     print(
#         f"Confidence Score: "
#         f"{validation.get('confidence_score', 0.0)}"
#     )

#     print(
#         f"Research Sufficient: "
#         f"{validation.get('research_sufficient', False)}"
#     )
    
#     # --------------------------------
#     # RETRY COUNT
#     # --------------------------------

#     retries = state.get(
#     "retries",
#     {}
# )
    
#     retry_count = retries.get(
#         "validator",
#         0
#     )
#     # --------------------------------
#     # STOP INFINITE RETRIES
#     # --------------------------------

#     if retry_count >= MAX_RETRIES:

#         print(
#             "\nMax retries reached."
#         )

#         return {

#             "validation":
#                 validation,
#             "vector_db":
#         state.get(
#             "vector_db"
#         ),

#             "next_agent":
#                 "reporter"
#         }

#     # --------------------------------
#     # VALIDATION FLAGS
#     # --------------------------------

#     research_sufficient = validation.get(
#         "research_sufficient",
#         False
#     )

#     needs_refinement = refinement.get(
#     "needs_refinement",
#     False
# )

#     refinement_type = refinement.get(
#     "refinement_type",
#     ""
# )

#     refinement_focus = refinement.get(
#     "refinement_focus",
#     []
# )
#     # =================================
#     # DETERMINE REAL RESEARCH QUALITY
#     # =================================

#     has_missing_sections = (
#         len(missing_sections) > 0
#     )

#     has_weak_sections = (
#         len(weak_sections) > 0
#     )

#     requires_refinement = (

#         needs_refinement

#         or has_missing_sections

#         or has_weak_sections
#     )
#     # =================================
#     # FORCE REFINEMENT IF NEEDED
#     # =================================
#     # print(missing_sections)
#     if requires_refinement:

#         print(
#             "\nValidator requested refinement."
#         )
#     # =================================
#     # SUCCESS CASE
#     # =================================

#     if (

#         research_sufficient

#         # and not requires_refinement

#     ):

#         return {

#             "validation":
#                 validation,

#             "validator_feedback":
#                 state.get(
#                     "validator_feedback",
#                     ""
#                 ),

#             "human_feedback":
#                 state.get(
#                     "human_feedback",
#                     ""
#                 ),
#                 "vector_db":
#         state.get(
#             "vector_db"
#         ),

#             "next_agent":
#                 "human_approval"
#         }
#     # --------------------------------
#     # BUILD FEEDBACK
#     # --------------------------------

#     feedback_parts = []

#     feedback_for_retry = refinement.get(
#     "feedback_for_retry",
#     ""
# )

#     if feedback_for_retry:

#         feedback_parts.append(
#             feedback_for_retry
#         )

#     feedback_parts.extend(
#         refinement_focus
#     )

#     weak_sections = issues.get(
#     "weak_sections",
#     []
# )

#     if weak_sections:

#         feedback_parts.append(

#             "Weak Sections: "
#             + ", ".join(weak_sections)
#         )

#     missing_sections = issues.get(
#     "missing_information",
#     []
# )

#     if missing_sections:

#         feedback_parts.append(

#             "Missing Sections: "
#             + ", ".join(missing_sections)
#         )

#     validator_feedback = "\n".join(
#         feedback_parts
#     )
  
#     # --------------------------------
#     # UPDATE ERRORS
#     # --------------------------------

#     errors = state.get(
#         "errors",
#         []
#     )

#     errors.append(
#         f"Validation refinement: "
#         f"{refinement_type}"
#     )
#     retries["validator"] = (
#     retry_count + 1
# )

#     # --------------------------------
#     # RETRIEVAL REFINEMENT
#     # --------------------------------

#     if refinement_type == "retrieval":

#         print(
#             "\nValidator requested "
#             "retrieval refinement."
#         )

#         return {

#         "validation":
#             validation,

#         "validator_feedback":
#             validator_feedback,

#         "human_feedback":
#             state.get(
#                 "human_feedback",
#                 ""
#             ),

#         "errors":
#             errors,
#         "retries":
#         retries,
#         "vector_db":
#         state.get(
#             "vector_db"
#         ),


#         "next_agent":
#             "decomposer"
#     }

#     # --------------------------------
#     # ANALYSIS REFINEMENT
#     # --------------------------------

#     print(
#         "\nValidator requested "
#         "analysis refinement."
#     )
#     return {

#     "validation":
#         validation,

#     "validator_feedback":
#         validator_feedback,

#     "human_feedback":
#         state.get(
#             "human_feedback",
#             ""
#         ),
#     "vector_db":
#         state.get(
#             "vector_db"
#         ),

#     "errors":
#         errors,

#     "retries":
#         retries,


#     "next_agent":
#         "analyzer"
# }
import json
import traceback

from models.llm_registry import (
    validator_llm
)

from prompts.validation import (
    VALIDATION_PROMPT
)

from schemas.output import (
    ValidationOutput
)

MAX_RETRIES = 5


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

    try:

        response = validator_llm.invoke(
            prompt
        )

        cleaned = response.content.strip()

        # =====================================
        # REMOVE MARKDOWN
        # =====================================

        cleaned = cleaned.replace(
            "```json",
            ""
        )

        cleaned = cleaned.replace(
            "```",
            ""
        ).strip()

        # =====================================
        # EXTRACT JSON ONLY
        # =====================================

        start = cleaned.find("{")

        end = cleaned.rfind("}")

        if start == -1 or end == -1:

            raise Exception(
                "Validator returned invalid JSON"
            )

        cleaned = cleaned[
            start:end + 1
        ]

        # =====================================
        # PARSE JSON
        # =====================================

        parsed = json.loads(
            cleaned
        )

        # =====================================
        # PYDANTIC VALIDATION
        # =====================================

        validation = ValidationOutput(
            **parsed
        ).model_dump()

    except Exception as e:

        traceback.print_exc()

        return {

            "critical_error": True,

            "workflow_complete": True,

            "awaiting_human_approval": False,

            "next_agent": "FINISH",

            "error": {

                "type": type(e).__name__,

                "message": str(e),

                "raw": traceback.format_exc()
            }
        }

    # --------------------------------
    # VALIDATION FIELDS
    # --------------------------------

    issues = validation.get(
        "issues",
        {}
    )

    refinement = validation.get(
        "refinement",
        {}
    )

    weak_sections = issues.get(
        "weak_sections",
        []
    )

    missing_sections = issues.get(
        "missing_information",
        []
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
    # RETRIES
    # --------------------------------

    retries = state.get(
        "retries",
        {}
    )

    retry_count = retries.get(
        "validator",
        0
    )

    # --------------------------------
    # STOP MAX RETRIES
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
    # FLAGS
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
    # QUALITY CHECKS
    # --------------------------------

    has_missing_sections = (
        len(missing_sections) > 0
    )

    has_weak_sections = (
        len(weak_sections) > 0
    )

    requires_refinement = (

        needs_refinement

        or has_missing_sections

        or has_weak_sections
    )

    # --------------------------------
    # SUCCESS CASE
    # --------------------------------

    if research_sufficient:

        return {

            "validation":
                validation,

            "validator_feedback":
                state.get(
                    "validator_feedback",
                    ""
                ),

            "human_feedback":
                state.get(
                    "human_feedback",
                    ""
                ),

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

    if weak_sections:

        feedback_parts.append(

            "Weak Sections: "
            + ", ".join(weak_sections)
        )

    if missing_sections:

        feedback_parts.append(

            "Missing Sections: "
            + ", ".join(missing_sections)
        )

    validator_feedback = "\n".join(
        feedback_parts
    )

    # --------------------------------
    # ERRORS
    # --------------------------------

    errors = state.get(
        "errors",
        []
    )

    errors.append(
        f"Validation refinement: "
        f"{refinement_type}"
    )

    retries["validator"] = (
        retry_count + 1
    )

    # --------------------------------
    # RETRIEVAL REFINEMENT
    # --------------------------------

    if refinement_type == "retrieval":

        print(
            "\nValidator requested retrieval refinement."
        )

        return {

            "validation":
                validation,

            "validator_feedback":
                validator_feedback,

            "human_feedback":
                state.get(
                    "human_feedback",
                    ""
                ),

            "errors":
                errors,

            "retries":
                retries,

            "next_agent":
                "decomposer"
        }

    # --------------------------------
    # ANALYSIS REFINEMENT
    # --------------------------------

    print(
        "\nValidator requested analysis refinement."
    )

    return {

        "validation":
            validation,

        "validator_feedback":
            validator_feedback,

        "human_feedback":
            state.get(
                "human_feedback",
                ""
            ),

        "errors":
            errors,

        "retries":
            retries,

        "next_agent":
            "analyzer"
    }