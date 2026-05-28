
from prompts.decomposition import (
    DECOMPOSITION_PROMPT
)

from datetime import datetime

from models.llm_registry import (
    fast_llm
)

from schemas.output import (
    DecompositionOutput
)

import traceback


structured_llm = (
    fast_llm.with_structured_output(
        DecompositionOutput
    )
)


def decomposition_agent(state):

    print(
        "\n========== DECOMPOSER ==========\n"
    )

    try:

        # =====================================
        # QUERY
        # =====================================

        query = state.get(
            "query",
            ""
        )

        # =====================================
        # VALIDATOR FEEDBACK
        # =====================================

        validator_feedback = state.get(
            "validator_feedback",
            ""
        )

        # =====================================
        # HUMAN FEEDBACK
        # =====================================

        human_feedback = state.get(
            "human_feedback",
            ""
        )

        # =====================================
        # CURRENT DATE
        # =====================================

        current_date = datetime.now().strftime(
            "%d-%m-%Y"
        )

        # =====================================
        # SECTION OPERATION
        # =====================================

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
        )

        # =====================================
        # ADD SECTION SPECIAL QUERY
        # =====================================

        if operation == "add":

            enhanced_query = f"""

Original Query:
{query}

New Section Needed:
{target_section}

Human Request:
{human_feedback}

Generate retrieval-focused subqueries
ONLY for the new requested section.

Do NOT regenerate old sections.

"""

        else:

            enhanced_query = query

        # =====================================
        # PROMPT
        # =====================================

        prompt = DECOMPOSITION_PROMPT.format(

            query=enhanced_query,

            validator_feedback=
                validator_feedback,

            human_feedback=
                human_feedback,

            current_date=
                current_date
        )

        print(
            "\n========== DECOMPOSITION PROMPT ==========\n"
        )

        print(prompt)

        # =====================================
        # LLM RESPONSE
        # =====================================

        response = structured_llm.invoke(
            prompt
        )

        if response is None:

            raise ValueError(
                "Decomposition returned empty response"
            )

        print(
            "\n========== RAW RESPONSE ==========\n"
        )

        print(response)

        result = response.model_dump()

        # =====================================
        # SUBQUERIES
        # =====================================

        subqueries = result.get(
            "subqueries",
            []
        )

        # =====================================
        # CLEAN SUBQUERIES
        # =====================================

        cleaned_subqueries = []

        seen = set()

        for subquery in subqueries:

            subquery = subquery.strip()

            if not subquery:

                continue

            normalized = subquery.lower()

            if normalized in seen:

                continue

            seen.add(normalized)

            cleaned_subqueries.append(
                subquery
            )

        # =====================================
        # LIMIT OUTPUT
        # =====================================

        cleaned_subqueries = (
            cleaned_subqueries[:6]
        )

        print(
            f"\nGenerated Subqueries: "
            f"{len(cleaned_subqueries)}"
        )

        for idx, subquery in enumerate(
            cleaned_subqueries
        ):

            print(
                f"{idx + 1}. {subquery}"
            )

        # =====================================
        # RETURN
        # =====================================

        return {

            "subqueries":
                cleaned_subqueries
        }

    except Exception as e:

        print(
            "\n========== DECOMPOSITION ERROR ==========\n"
        )

        print(str(e))

        print(
            "\n========== TRACEBACK ==========\n"
        )

        traceback.print_exc()

        raise

