from datetime import datetime

from models.llm_registry import (
    report_llm
)

from prompts.reporting import (
    REPORT_PROMPT
)

from schemas.output import (
    ReportOutput
)

import json
import traceback
import re


def reporting_agent(state):

    try:

        print(
            "\n========== REPORT AGENT ==========\n"
        )

        # =====================================
        # LOAD STATE
        # =====================================

        analysis = state.get(
            "analysis",
            {}
        )

        previous_analysis = state.get(
            "previous_analysis",
            {}
        ) or {}

        previous_report = state.get(
            "previous_report",
            {}
        ) or {}

        findings = analysis.get(
            "key_findings",
            []
        )

        dynamic_sections = (

            analysis.get(
                "dynamic_sections"
            )

            or previous_analysis.get(
                "dynamic_sections",
                []
            )

            or previous_report.get(
                "dynamic_sections",
                []
            )
        )

        print(
            "\n========== INITIAL SECTIONS ==========\n"
        )

        print([
            section.get("heading")
            for section in dynamic_sections
        ])

        # =====================================
        # OPERATION
        # =====================================

        section_operation = state.get(
            "section_operation",
            {}
        )

        operation = str(
            section_operation.get(
                "operation",
                "none"
            )
        ).strip().lower()

        target_section = str(
            section_operation.get(
                "target_section",
                ""
            )
        ).strip().lower()

        print(
            "\n========== OPERATION ==========\n"
        )

        print(operation)

        print(target_section)

        # =====================================
        # DELETE SECTION
        # =====================================

        if operation == "delete":

            filtered_sections = []

            normalized_target = re.sub(
                r"\s+",
                " ",
                target_section
            )

            for section in dynamic_sections:

                heading = str(
                    section.get(
                        "heading",
                        ""
                    )
                ).strip().lower()

                normalized_heading = re.sub(
                    r"\s+",
                    " ",
                    heading
                )

                print(
                    f"\nCOMPARE => "
                    f"{normalized_heading} "
                    f"vs "
                    f"{normalized_target}"
                )

                # =================================
                # KEEP ALL OTHER SECTIONS
                # =================================

                if normalized_target not in normalized_heading:

                    filtered_sections.append(
                        section
                    )

                else:

                    print(
                        f"\nDELETED => "
                        f"{heading}"
                    )

            dynamic_sections = filtered_sections

            analysis[
                "dynamic_sections"
            ] = filtered_sections

        print(
            "\n========== FINAL SECTIONS ==========\n"
        )

        print([
            section.get("heading")
            for section in dynamic_sections
        ])
        if operation == "delete":

            return {
            
                "analysis":
                    analysis,

                # "report":
                #     report,

                "awaiting_human_approval":
                    True,

                "workflow_complete":
                    False,
                "next_agent":
                    "human_approval"
            }

        # =====================================
        # TRIM SECTIONS
        # =====================================

        trimmed_sections = []

        for section in dynamic_sections:

            trimmed_sections.append({

                "heading":
                    section.get(
                        "heading",
                        ""
                    ),

                "content":
                    section.get(
                        "content",
                        ""
                    )[:1500],

                "citations":
                    section.get(
                        "citations",
                        []
                    )[:10]
            })

        citations = []

        for section in trimmed_sections:

            for citation in section.get(
                "citations",
                []
            ):

                if citation not in citations:

                    citations.append(
                        citation
                    )

        current_date = datetime.now().strftime(
            "%d-%m-%Y"
        )

        query = str(
            state.get(
                "query",
                ""
            )
        )

        human_feedback = str(
            state.get(
                "human_feedback",
                ""
            )
        )

        # =====================================
        # PROMPT
        # =====================================

        prompt = REPORT_PROMPT.format(

            current_date=current_date,

            query=query,

            findings=json.dumps(
                findings
            ),

            dynamic_sections=json.dumps(
                trimmed_sections
            ),

            citations=json.dumps(
                citations
            ),

            human_feedback=human_feedback
        )

        raw_response = report_llm.invoke(
            prompt
        )

        content = ""

        if hasattr(raw_response, "content"):

            content = str(
                raw_response.content
            )

        else:

            content = str(raw_response)

        cleaned = content.strip()

        cleaned = cleaned.replace(
            "```json",
            ""
        )

        cleaned = cleaned.replace(
            "```",
            ""
        ).strip()

        json_match = re.search(

            r'\{.*\}',

            cleaned,

            re.DOTALL
        )

        if not json_match:

            raise ValueError(
                "No JSON found in report response"
            )

        json_text = json_match.group(0)

        parsed = json.loads(
            json_text
        )

        report = ReportOutput(
            **parsed
        ).model_dump()

        # =====================================
        # FORCE FINAL FILTERED SECTIONS
        # =====================================

        report[
            "dynamic_sections"
        ] = dynamic_sections

        print(
            "\n========== FINAL REPORT ==========\n"
        )

        print([
            section.get("heading")
            for section in report[
                "dynamic_sections"
            ]
        ])
        

        return {
        
            "analysis":
                analysis,

            "report":
                report,

            "workflow_complete":
                    True,

            "next_agent":
                    "END"
        }

        # return {

        #     "analysis":
        #         analysis,

        #     "report":
        #         report,

        #     "workflow_complete":
        #         True,

        #     "next_agent":
        #         "END"
        # }
#         return {

#     "analysis":
#         analysis,

#     "report":
#         report,

#     "awaiting_human_approval":
#         True,

#     "workflow_complete":
#         False,

#     # "next_agent":
#     #     "human_approval"
# }

    except Exception as e:

        print(
            "\n========== REPORT ERROR ==========\n"
        )

        print(
            "\nERROR TYPE:"
        )

        print(
            type(e).__name__
        )

        print(
            "\nERROR MESSAGE:"
        )

        print(
            str(e)
        )

        print(
            "\nTRACEBACK:"
        )

        print(
            traceback.format_exc()
        )

        traceback.print_exc()

        # =====================================
        # IMPORTANT
        # Let safe_execute() handle all errors
        # =====================================

        raise