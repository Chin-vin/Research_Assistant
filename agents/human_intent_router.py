# # # from prompts.human_router import (
# # #     HUMAN_ROUTER_PROMPT
# # # )

# # # from models.llm_registry import (
# # #     fast_llm
# # # )

# # # from schemas.output import (
# # #     HumanIntentOutput
# # # )


# # # structured_llm = (

# # #     fast_llm.with_structured_output(
# # #         HumanIntentOutput
# # #     )
# # # )


# # # def human_intent_router_agent(state):

# # #     feedback = state.get(
# # #         "human_feedback",
# # #         ""
# # #     )

# # #     prompt = HUMAN_ROUTER_PROMPT.format(

# # #         feedback=feedback
# # #     )

# # #     response = structured_llm.invoke(
# # #         prompt
# # #     )

# # #     result = response.model_dump()

# # #     target_agent = result.get(
# # #         "target_agent",
# # #         "analyzer"
# # #     )

# # #     section_operation = result.get(
# # #         "section_operation",
# # #         {
# # #             "operation": "none",
# # #             "target_section": "",
# # #             "section_description": ""
# # #         }
# # #     )

# # #     return {

# # #     "next_agent":
# # #         target_agent,

# # #     "section_operation":
# # #         section_operation,

# # #     "previous_analysis":
# # #         state.get(
# # #             "analysis",
# # #             {}
# # #         ),

# # #     "previous_report":
# # #         state.get(
# # #             "report",
# # #             {}
# # #         )
# # # }c
# # import json
# # import re
# # import traceback

# # from groq import (
# #     RateLimitError,
# #     APITimeoutError,
# #     APIConnectionError,
# #     BadRequestError
# # )

# # from prompts.human_router import (
# #     HUMAN_ROUTER_PROMPT
# # )

# # from models.llm_registry import (
# #     fast_llm
# # )


# # def human_intent_router_agent(state):

# #     try:

# #         print(
# #             "\n========== HUMAN INTENT ROUTER ==========\n"
# #         )

# #         feedback = state.get(
# #             "human_feedback",
# #             ""
# #         )

# #         prompt = HUMAN_ROUTER_PROMPT.format(

# #             feedback=feedback
# #         )

# #         # =====================================
# #         # RAW INVOKE
# #         # =====================================

# #         raw_response = fast_llm.invoke(
# #             prompt
# #         )

# #         print(
# #             "\n========== RAW RESPONSE ==========\n"
# #         )

# #         print(raw_response)

# #         # =====================================
# #         # SAFE CONTENT EXTRACTION
# #         # =====================================

# #         content = ""

# #         if hasattr(
# #             raw_response,
# #             "content"
# #         ):

# #             if isinstance(
# #                 raw_response.content,
# #                 str
# #             ):

# #                 content = raw_response.content

# #             elif isinstance(
# #                 raw_response.content,
# #                 list
# #             ):

# #                 for item in raw_response.content:

# #                     if isinstance(
# #                         item,
# #                         dict
# #                     ):

# #                         content += item.get(
# #                             "text",
# #                             ""
# #                         )

# #                     else:

# #                         content += str(item)

# #             else:

# #                 content = str(
# #                     raw_response.content
# #                 )

# #         else:

# #             content = str(
# #                 raw_response
# #             )

# #         print(
# #             "\n========== CONTENT ==========\n"
# #         )

# #         print(content)

# #         # =====================================
# #         # EMPTY CHECK
# #         # =====================================

# #         if not content.strip():

# #             raise ValueError(
# #                 "Empty router response"
# #             )

# #         # =====================================
# #         # REMOVE MARKDOWN
# #         # =====================================

# #         cleaned = content.strip()

# #         cleaned = cleaned.replace(
# #             "```json",
# #             ""
# #         )

# #         cleaned = cleaned.replace(
# #             "```",
# #             ""
# #         ).strip()

# #         # =====================================
# #         # EXTRACT JSON
# #         # =====================================

# #         json_match = re.search(

# #             r'\{.*\}',

# #             cleaned,

# #             re.DOTALL
# #         )

# #         if not json_match:

# #             raise ValueError(
# #                 "No valid JSON found in router response"
# #             )

# #         json_text = json_match.group(0)

# #         print(
# #             "\n========== JSON ==========\n"
# #         )

# #         print(json_text)

# #         # =====================================
# #         # PARSE JSON
# #         # =====================================

# #         result = json.loads(
# #             json_text
# #         )

# #         # =====================================
# #         # SAFE EXTRACTION
# #         # =====================================

# #         target_agent = result.get(
# #             "target_agent",
# #             "analyzer"
# #         )

# #         operation = result.get(
# #             "operation",
# #             "none"
# #         )

# #         target_section = result.get(
# #             "target_section",
# #             ""
# #         )

# #         reference_section = result.get(
# #             "reference_section",
# #             ""
# #         )

# #         position = result.get(
# #             "position",
# #             ""
# #         )

# #         print(
# #             "\n========== ROUTER SUCCESS ==========\n"
# #         )

# #         return {

# #             "next_agent":
# #                 target_agent,

# #             "operation":
# #                 operation,

# #             "target_section":
# #                 target_section,

# #             "reference_section":
# #                 reference_section,

# #             "position":
# #                 position,

# #             "previous_analysis":
# #                 state.get(
# #                     "analysis",
# #                     {}
# #                 ),

# #             "previous_report":
# #                 state.get(
# #                     "report",
# #                     {}
# #                 )
# #         }

# #     except Exception as e:

# #         print(
# #             "\n========== ROUTER ERROR ==========\n"
# #         )

# #         traceback.print_exc()

# #         # =====================================
# #         # ERROR TYPE
# #         # =====================================

# #         if isinstance(
# #             e,
# #             RateLimitError
# #         ):

# #             error_title = (
# #                 "Rate Limit Exceeded"
# #             )

# #         elif isinstance(
# #             e,
# #             APITimeoutError
# #         ):

# #             error_title = (
# #                 "Request Timeout"
# #             )

# #         elif isinstance(
# #             e,
# #             APIConnectionError
# #         ):

# #             error_title = (
# #                 "API Connection Error"
# #             )

# #         elif isinstance(
# #             e,
# #             BadRequestError
# #         ):

# #             error_title = (
# #                 "Bad Request Error"
# #             )

# #         elif isinstance(
# #             e,
# #             json.JSONDecodeError
# #         ):

# #             error_title = (
# #                 "JSON Parsing Failed"
# #             )

# #         else:

# #             error_title = type(e).__name__

# #         return {

# #             "critical_error": True,

# #             "workflow_complete": True,

# #             "next_agent": "FINISH",

# #             "error": {

# #                 "type": error_title,

# #                 "message": str(e),

# #                 "raw": traceback.format_exc()
# #             }
# #         }
# import json
# import re
# import traceback

# from groq import (
#     RateLimitError,
#     APITimeoutError,
#     APIConnectionError,
#     BadRequestError
# )

# from prompts.human_router import (
#     HUMAN_ROUTER_PROMPT
# )

# from models.llm_registry import (
#     fast_llm
# )


# def human_intent_router_agent(state):

#     try:

#         print(
#             "\n========== HUMAN INTENT ROUTER ==========\n"
#         )

#         # =====================================
#         # HUMAN FEEDBACK
#         # =====================================

#         feedback = state.get(
#             "human_feedback",
#             ""
#         )

#         # =====================================
#         # PROMPT
#         # =====================================

#         prompt = HUMAN_ROUTER_PROMPT.format(

#             feedback=feedback
#         )

#         # =====================================
#         # RAW INVOKE
#         # =====================================

#         raw_response = fast_llm.invoke(
#             prompt
#         )

#         print(
#             "\n========== RAW RESPONSE ==========\n"
#         )

#         print(raw_response)

#         # =====================================
#         # SAFE CONTENT EXTRACTION
#         # =====================================

#         content = ""

#         if hasattr(
#             raw_response,
#             "content"
#         ):

#             if isinstance(
#                 raw_response.content,
#                 str
#             ):

#                 content = raw_response.content

#             elif isinstance(
#                 raw_response.content,
#                 list
#             ):

#                 for item in raw_response.content:

#                     if isinstance(
#                         item,
#                         dict
#                     ):

#                         content += item.get(
#                             "text",
#                             ""
#                         )

#                     else:

#                         content += str(item)

#             else:

#                 content = str(
#                     raw_response.content
#                 )

#         else:

#             content = str(
#                 raw_response
#             )

#         print(
#             "\n========== CONTENT ==========\n"
#         )

#         print(content)

#         # =====================================
#         # EMPTY RESPONSE
#         # =====================================

#         if not content.strip():

#             raise ValueError(
#                 "Empty router response"
#             )

#         # =====================================
#         # REMOVE MARKDOWN
#         # =====================================

#         cleaned = content.strip()

#         cleaned = cleaned.replace(
#             "```json",
#             ""
#         )

#         cleaned = cleaned.replace(
#             "```",
#             ""
#         ).strip()

#         # =====================================
#         # EXTRACT JSON
#         # =====================================

#         json_match = re.search(

#             r'\{.*\}',

#             cleaned,

#             re.DOTALL
#         )

#         # =====================================
#         # FALLBACK ROUTING
#         # =====================================

#         if not json_match:

#             print(
#                 "\nNO JSON FOUND -> FALLBACK ROUTER\n"
#             )

#             lower_feedback = feedback.lower()

#             # =================================
#             # ADD SECTION
#             # =================================

#             if any(
#                 word in lower_feedback

#                 for word in [

#                     "add section",
#                     "include section",
#                     "new section",
#                     "add topic"
#                 ]
#             ):

#                 return {

#                     "next_agent":
#                         "analyzer",

#                     "operation":
#                         "ADD_SECTION",

#                     "target_section":
#                         "",

#                     "reference_section":
#                         "",

#                     "position":
#                         "",

#                     "previous_analysis":
#                         state.get(
#                             "analysis",
#                             {}
#                         ),

#                     "previous_report":
#                         state.get(
#                             "report",
#                             {}
#                         )
#                 }

#             # =================================
#             # DELETE SECTION
#             # =================================

#             elif any(
#                 word in lower_feedback

#                 for word in [

#                     "delete",
#                     "remove section",
#                     "remove topic"
#                 ]
#             ):

#                 return {

#                     "next_agent":
#                         "reporter",

#                     "operation":
#                         "DELETE_SECTION",

#                     "target_section":
#                         feedback,

#                     "reference_section":
#                         "",

#                     "position":
#                         "",

#                     "previous_analysis":
#                         state.get(
#                             "analysis",
#                             {}
#                         ),

#                     "previous_report":
#                         state.get(
#                             "report",
#                             {}
#                         )
#                 }

#             # =================================
#             # UPDATE SECTION
#             # =================================

#             elif any(
#                 word in lower_feedback

#                 for word in [

#                     "expand",
#                     "update",
#                     "modify",
#                     "improve"
#                 ]
#             ):

#                 return {

#                     "next_agent":
#                         "analyzer",

#                     "operation":
#                         "UPDATE_SECTION",

#                     "target_section":
#                         "",

#                     "reference_section":
#                         "",

#                     "position":
#                         "",

#                     "previous_analysis":
#                         state.get(
#                             "analysis",
#                             {}
#                         ),

#                     "previous_report":
#                         state.get(
#                             "report",
#                             {}
#                         )
#                 }

#             # =================================
#             # REORDER SECTION
#             # =================================

#             elif any(
#                 word in lower_feedback

#                 for word in [

#                     "move",
#                     "reorder",
#                     "place after",
#                     "place before"
#                 ]
#             ):

#                 return {

#                     "next_agent":
#                         "reporter",

#                     "operation":
#                         "REORDER_SECTION",

#                     "target_section":
#                         "",

#                     "reference_section":
#                         "",

#                     "position":
#                         "",

#                     "previous_analysis":
#                         state.get(
#                             "analysis",
#                             {}
#                         ),

#                     "previous_report":
#                         state.get(
#                             "report",
#                             {}
#                         )
#                 }

#             # =================================
#             # DEFAULT
#             # =================================

#             return {

#                 "next_agent":
#                     "analyzer",

#                 "operation":
#                     "NONE",

#                 "target_section":
#                     "",

#                 "reference_section":
#                     "",

#                 "position":
#                     "",

#                 "previous_analysis":
#                     state.get(
#                         "analysis",
#                         {}
#                     ),

#                 "previous_report":
#                     state.get(
#                         "report",
#                         {}
#                     )
#             }

#         # =====================================
#         # JSON FOUND
#         # =====================================

#         json_text = json_match.group(0)

#         print(
#             "\n========== JSON ==========\n"
#         )

#         print(json_text)

#         # =====================================
#         # PARSE JSON
#         # =====================================

#         result = json.loads(
#             json_text
#         )

#         # =====================================
#         # SAFE EXTRACTION
#         # =====================================

#         target_agent = result.get(
#             "target_agent",
#             "analyzer"
#         )

#         operation = result.get(
#             "operation",
#             "NONE"
#         )

#         target_section = result.get(
#             "target_section",
#             ""
#         )

#         reference_section = result.get(
#             "reference_section",
#             ""
#         )

#         position = result.get(
#             "position",
#             ""
#         )

#         print(
#             "\n========== ROUTER SUCCESS ==========\n"
#         )

#         return {

#     "next_agent":
#         target_agent,

#     "section_operation": {

#         "operation":
#             str(operation).lower(),

#         "target_section":
#             str(target_section).lower(),

#         "reference_section":
#             str(reference_section).lower(),

#         "position":
#             str(position).lower()
#     },

#     "previous_analysis":
#         state.get(
#             "analysis",
#             {}
#         ),

#     "previous_report":
#         state.get(
#             "report",
#             {}
#         )
# }

#     except Exception as e:

#         print(
#             "\n========== ROUTER ERROR ==========\n"
#         )

#         traceback.print_exc()

#         # =====================================
#         # ERROR TYPE
#         # =====================================

#         if isinstance(
#             e,
#             RateLimitError
#         ):

#             error_title = (
#                 "Rate Limit Exceeded"
#             )

#         elif isinstance(
#             e,
#             APITimeoutError
#         ):

#             error_title = (
#                 "Request Timeout"
#             )

#         elif isinstance(
#             e,
#             APIConnectionError
#         ):

#             error_title = (
#                 "API Connection Error"
#             )

#         elif isinstance(
#             e,
#             BadRequestError
#         ):

#             error_title = (
#                 "Bad Request Error"
#             )

#         elif isinstance(
#             e,
#             json.JSONDecodeError
#         ):

#             error_title = (
#                 "JSON Parsing Failed"
#             )

#         else:

#             error_title = type(e).__name__

#         return {

#             "critical_error": True,

#             "workflow_complete": True,

#             "next_agent": "FINISH",

#             "error": {

#                 "type": error_title,

#                 "message": str(e),

#                 "raw": traceback.format_exc()
#             }
#         }
import json
import re
import traceback

from prompts.human_router import (
    HUMAN_ROUTER_PROMPT
)

from models.llm_registry import (
    fast_llm
)


def human_intent_router_agent(state):

    try:

        print(
            "\n========== HUMAN INTENT ROUTER ==========\n"
        )

        feedback = str(
            state.get(
                "human_feedback",
                ""
            )
        )

        prompt = HUMAN_ROUTER_PROMPT.format(
            feedback=feedback
        )

        raw_response = fast_llm.invoke(
            prompt
        )

        content = ""

        if hasattr(raw_response, "content"):

            if isinstance(
                raw_response.content,
                str
            ):

                content = raw_response.content

            else:

                content = str(
                    raw_response.content
                )

        else:

            content = str(raw_response)

        print(
            "\n========== RAW ROUTER RESPONSE ==========\n"
        )

        print(content)

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
                "No valid JSON found"
            )

        json_text = json_match.group(0)

        result = json.loads(
            json_text
        )

        print(
            "\n========== PARSED ROUTER JSON ==========\n"
        )

        print(
            json.dumps(
                result,
                indent=2
            )
        )

        # =====================================
        # SAFE EXTRACTION
        # =====================================

        target_agent = str(
            result.get(
                "target_agent",
                "analyzer"
            )
        ).strip()

        section_operation = result.get(
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

        section_description = str(
            section_operation.get(
                "section_description",
                ""
            )
        ).strip()

        # =====================================
        # NORMALIZE OPERATION
        # =====================================

        if "delete" in operation:

            operation = "delete"

        elif "add" in operation:

            operation = "add"

        elif "update" in operation:

            operation = "update"

        else:

            operation = "none"

        final_result = {

            "next_agent":
                target_agent,

            "section_operation": {

                "operation":
                    operation,

                "target_section":
                    target_section,

                "section_description":
                    section_description
            },

            "previous_analysis":
                state.get(
                    "analysis",
                    {}
                ),

            "previous_report":
                state.get(
                    "report",
                    {}
                )
        }

        print(
            "\n========== FINAL ROUTER STATE ==========\n"
        )

        print(
            json.dumps(
                final_result,
                indent=2
            )
        )

        return final_result

    except Exception as e:

        print(
            "\n========== ROUTER ERROR ==========\n"
        )

        traceback.print_exc()

        return {

            "critical_error": True,

            "workflow_complete": True,

            "next_agent": "FINISH",

            "error": {

                "type": type(e).__name__,

                "message": str(e),

                "raw": traceback.format_exc()
            }
        }