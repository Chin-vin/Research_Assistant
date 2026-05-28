# # # # # # # from datetime import (
# # # # # # #     datetime
# # # # # # # )

# # # # # # # from models.llm_registry import (
# # # # # # #     report_llm
# # # # # # # )

# # # # # # # from prompts.reporting import (
# # # # # # #     REPORT_PROMPT
# # # # # # # )

# # # # # # # from schemas.output import (
# # # # # # #     ReportOutput
# # # # # # # )



# # # # # # # structured_llm = (
# # # # # # #     report_llm.with_structured_output(
# # # # # # #         ReportOutput
# # # # # # #     )
# # # # # # # )


# # # # # # # def reporting_agent(state):
# # # # # # #     print("Rport agent")
# # # # # # #     # --------------------------------
# # # # # # #     # ANALYSIS
# # # # # # #     # --------------------------------

# # # # # # #     analysis = state.get(
# # # # # # #         "analysis",
# # # # # # #         {}
# # # # # # #     )

# # # # # # #     # --------------------------------
# # # # # # #     # SAFE FIELD EXTRACTION
# # # # # # #     # --------------------------------

# # # # # # #     findings = analysis.get(
# # # # # # #         "key_findings",
# # # # # # #         []
# # # # # # #     )

# # # # # # #     # --------------------------------
# # # # # # #     # DYNAMIC SECTIONS
# # # # # # #     # --------------------------------
# # # # # # #     dynamic_sections = analysis.get(
# # # # # # #     "dynamic_sections",
# # # # # # #     []
# # # # # # # )

# # # # # # #     section_operation = state.get(
# # # # # # #         "section_operation",
# # # # # # #         {}
# # # # # # #     )

# # # # # # #     operation = section_operation.get(
# # # # # # #         "operation",
# # # # # # #         "none"
# # # # # # #     )

# # # # # # #     target_section = section_operation.get(
# # # # # # #         "target_section",
# # # # # # #         ""
# # # # # # #     ).strip().lower()

# # # # # # #     if operation == "delete":

# # # # # # #         filtered_sections = []

# # # # # # #         for section in dynamic_sections:

# # # # # # #             heading = section.get(
# # # # # # #                 "heading",
# # # # # # #                 ""
# # # # # # #             ).strip().lower()

# # # # # # #             if heading != target_section:

# # # # # # #                 filtered_sections.append(
# # # # # # #                     section
# # # # # # #                 )

# # # # # # #         analysis[
# # # # # # #             "dynamic_sections"
# # # # # # #         ] = filtered_sections

# # # # # # #         existing_report = state.get(
# # # # # # #             "report",
# # # # # # #             {}
# # # # # # #         )

# # # # # # #         existing_report[
# # # # # # #             "dynamic_sections"
# # # # # # #         ] = filtered_sections

# # # # # # #         return {

# # # # # # #             "analysis":
# # # # # # #                 analysis,

# # # # # # #             "report":
# # # # # # #                 existing_report,

# # # # # # #             "workflow_complete":
# # # # # # #                 True,

# # # # # # #             "next_agent":
# # # # # # #                 "FINISH"
# # # # # # #         }
# # # # # # #     citations=[]
# # # # # # #     for section in dynamic_sections:

# # # # # # #         section_citations = section.get(
# # # # # # #             "citations",
# # # # # # #             []
# # # # # # #         )

# # # # # # #         for citation in section_citations:

# # # # # # #             if citation not in citations:

# # # # # # #                 citations.append(citation)
# # # # # # #     # --------------------------------
# # # # # # #     # CURRENT DATE
# # # # # # #     # --------------------------------

# # # # # # #     current_date = datetime.now().strftime(
# # # # # # #         "%d-%m-%Y"
# # # # # # #     )

# # # # # # #     # --------------------------------
# # # # # # #     # QUERY
# # # # # # #     # --------------------------------

# # # # # # #     query = state.get(
# # # # # # #         "query",
# # # # # # #         ""
# # # # # # #     )

# # # # # # #     human_feedback = state.get(
# # # # # # #     "human_feedback",
# # # # # # #     ""
# # # # # # # )
# # # # # # #     # --------------------------------
# # # # # # #     # PROMPT
# # # # # # #     # --------------------------------

# # # # # # #     prompt = REPORT_PROMPT.format(

# # # # # # #     current_date=current_date,

# # # # # # #     query=query,

# # # # # # #     findings=findings,

# # # # # # #     dynamic_sections=dynamic_sections,

# # # # # # #     citations=citations,

# # # # # # #     human_feedback=human_feedback
# # # # # # # )


# # # # # # #     print(
# # # # # # #         f"\nCitations Count: "
# # # # # # #         f"{len(citations)}"
# # # # # # #     )
    
# # # # # # #     # --------------------------------
# # # # # # #     # GENERATE REPORT
# # # # # # #     # --------------------------------

# # # # # # #     try:

# # # # # # #         response = structured_llm.invoke(
# # # # # # #             prompt
# # # # # # #         )

# # # # # # #         report = response.model_dump()

# # # # # # #         report["dynamic_sections"] = (
# # # # # # #             dynamic_sections
# # # # # # #         )

# # # # # # #     except Exception as e:
        
# # # # # # #         print(
# # # # # # #             f"\nReport Generation Error: {e}"
# # # # # # #         )
    
# # # # # # #         return {
        
# # # # # # #             "critical_error": True,
    
# # # # # # #             "errors": [
# # # # # # #                 str(e)
# # # # # # #             ],
    
# # # # # # #             "workflow_complete": True,
    
# # # # # # #             "next_agent": "FINISH"
# # # # # # #         }

# # # # # # #     # --------------------------------
# # # # # # #     # RETURN
# # # # # # #     # --------------------------------

# # # # # # #     return {

# # # # # # #         "report": report,

# # # # # # #         "workflow_complete": True,

# # # # # # #         "next_agent": "FINISH"
# # # # # # #     }
# # # # # # from datetime import (
# # # # # #     datetime
# # # # # # )

# # # # # # from models.llm_registry import (
# # # # # #     report_llm
# # # # # # )

# # # # # # from prompts.reporting import (
# # # # # #     REPORT_PROMPT
# # # # # # )

# # # # # # from schemas.output import (
# # # # # #     ReportOutput
# # # # # # )


# # # # # # structured_llm = (
# # # # # #     report_llm.with_structured_output(
# # # # # #         ReportOutput
# # # # # #     )
# # # # # # )


# # # # # # def reporting_agent(state):

# # # # # #     print("Report agent")

# # # # # #     # --------------------------------
# # # # # #     # ANALYSIS
# # # # # #     # --------------------------------

# # # # # #     analysis = state.get(
# # # # # #         "analysis",
# # # # # #         {}
# # # # # #     )

# # # # # #     findings = analysis.get(
# # # # # #         "key_findings",
# # # # # #         []
# # # # # #     )

# # # # # #     dynamic_sections = analysis.get(
# # # # # #         "dynamic_sections",
# # # # # #         []
# # # # # #     )

# # # # # #     # =====================================
# # # # # #     # SECTION OPERATION
# # # # # #     # =====================================

# # # # # #     section_operation = state.get(
# # # # # #         "section_operation",
# # # # # #         {}
# # # # # #     )

# # # # # #     operation = section_operation.get(
# # # # # #         "operation",
# # # # # #         "none"
# # # # # #     )

# # # # # #     target_section = section_operation.get(
# # # # # #         "target_section",
# # # # # #         ""
# # # # # #     ).strip().lower()

# # # # # #     # =====================================
# # # # # #     # DELETE SECTION ONLY
# # # # # #     # =====================================

# # # # # #     if operation == "delete":

# # # # # #         filtered_sections = []

# # # # # #         for section in dynamic_sections:

# # # # # #             heading = section.get(
# # # # # #                 "heading",
# # # # # #                 ""
# # # # # #             ).strip().lower()

# # # # # #             # =================================
# # # # # #             # KEEP ALL OTHER SECTIONS
# # # # # #             # =================================

# # # # # #             if heading != target_section:

# # # # # #                 filtered_sections.append(
# # # # # #                     section
# # # # # #                 )

# # # # # #         # =====================================
# # # # # #         # UPDATE ANALYSIS
# # # # # #         # =====================================

# # # # # #         analysis[
# # # # # #             "dynamic_sections"
# # # # # #         ] = filtered_sections

# # # # # #         # IMPORTANT
# # # # # #         dynamic_sections = filtered_sections

# # # # # #     # =====================================
# # # # # #     # CITATIONS
# # # # # #     # =====================================

# # # # # #     citations = []

# # # # # #     for section in dynamic_sections:

# # # # # #         section_citations = section.get(
# # # # # #             "citations",
# # # # # #             []
# # # # # #         )

# # # # # #         for citation in section_citations:

# # # # # #             if citation not in citations:

# # # # # #                 citations.append(
# # # # # #                     citation
# # # # # #                 )

# # # # # #     # --------------------------------
# # # # # #     # CURRENT DATE
# # # # # #     # --------------------------------

# # # # # #     current_date = datetime.now().strftime(
# # # # # #         "%d-%m-%Y"
# # # # # #     )

# # # # # #     # --------------------------------
# # # # # #     # QUERY
# # # # # #     # --------------------------------

# # # # # #     query = state.get(
# # # # # #         "query",
# # # # # #         ""
# # # # # #     )

# # # # # #     human_feedback = state.get(
# # # # # #         "human_feedback",
# # # # # #         ""
# # # # # #     )

# # # # # #     # =====================================
# # # # # #     # PROMPT
# # # # # #     # =====================================

# # # # # #     prompt = REPORT_PROMPT.format(

# # # # # #         current_date=current_date,

# # # # # #         query=query,

# # # # # #         findings=findings,

# # # # # #         dynamic_sections=dynamic_sections,

# # # # # #         citations=citations,

# # # # # #         human_feedback=human_feedback
# # # # # #     )

# # # # # #     print(
# # # # # #         f"\nCitations Count: "
# # # # # #         f"{len(citations)}"
# # # # # #     )

# # # # # #     # =====================================
# # # # # #     # GENERATE REPORT
# # # # # #     # =====================================

# # # # # #     try:

# # # # # #         response = structured_llm.invoke(
# # # # # #             prompt
# # # # # #         )
# # # # # #         print("hello")
# # # # # #         report = response.model_dump()
# # # # # #         print("report")
# # # # # #         print(report)
# # # # # #         # =====================================
# # # # # #         # PRESERVE FILTERED SECTIONS
# # # # # #         # =====================================

# # # # # #         report[
# # # # # #             "dynamic_sections"
# # # # # #         ] = dynamic_sections

# # # # # #     except Exception as e:

# # # # # #         print(
# # # # # #             f"\nReport Generation Error: {e}"
# # # # # #         )

# # # # # #         return {

# # # # # #             "critical_error": True,

# # # # # #             "errors": [
# # # # # #                 str(e)
# # # # # #             ],

# # # # # #             "workflow_complete": True,

# # # # # #             "next_agent": "FINISH"
# # # # # #         }

# # # # # #     # =====================================
# # # # # #     # RETURN
# # # # # #     # =====================================

# # # # # #     return {

# # # # # #         "analysis":
# # # # # #             analysis,

# # # # # #         "report":
# # # # # #             report,

# # # # # #         "workflow_complete":
# # # # # #             True,

# # # # # #         "next_agent":
# # # # # #             "FINISH"
# # # # # #     }
# # # # # # # REPORT_PROMPT = """

# # # # # # # You are an expert Research Report
# # # # # # # Generation Agent specialized in generating:

# # # # # # # - professional research reports
# # # # # # # - technical whitepapers
# # # # # # # - analytical industry reports
# # # # # # # - research synthesis documents

# # # # # # # CURRENT DATE:
# # # # # # # {current_date}


# # # # # # # Generate a research-paper-style report.

# # # # # # # The report MUST contain:

# # # # # # # 1. Title
# # # # # # # 2. Abstract
# # # # # # # 3. Keywords
# # # # # # # 4. Introduction
# # # # # # # 5.Literature Review
# # # # # # # 6.Methodology
# # # # # # # 7. Dynamically Generated Sections
# # # # # # # 8. Conclusion
# # # # # # # 9. References

# # # # # # # IMPORTANT:

# # # # # # # - Dynamically generate ONLY sections
# # # # # # #   relevant to the query and evidence.

# # # # # # # - Section headings should adapt
# # # # # # #   intelligently to:
# # # # # # #   - domain
# # # # # # #   - retrieved evidence
# # # # # # #   - technical depth
# # # # # # #   - user intent

# # # # # # # Examples:

# # # # # # # Blockchain:
# # # # # # # - Consensus Mechanisms
# # # # # # # - Smart Contract Security
# # # # # # # - Decentralization Challenges

# # # # # # # Artificial Intelligence:
# # # # # # # - LLM Architectures
# # # # # # # - Agentic Systems
# # # # # # # - Ethical Concerns

# # # # # # # Healthcare:
# # # # # # # - Clinical Applications
# # # # # # # - Patient Outcomes
# # # # # # # - Regulatory Challenges

# # # # # # # Cybersecurity:
# # # # # # # - Threat Detection
# # # # # # # - Zero Trust Architectures
# # # # # # # - Security Limitations

# # # # # # # Education:
# # # # # # # - Personalized Learning
# # # # # # # - Learning Analytics
# # # # # # # - Student Engagement

# # # # # # # DO NOT generate:
# # # # # # # - irrelevant sections
# # # # # # # - empty sections
# # # # # # # - placeholder content

# # # # # # # Each dynamic section must contain:
# # # # # # # - detailed analysis
# # # # # # # - technical depth
# # # # # # # - evidence-backed reasoning
# # # # # # # - professional academic tone

# # # # # # # Your task is to generate a HIGH-QUALITY,
# # # # # # # DETAILED, and QUERY-ADAPTIVE report
# # # # # # # based on the provided research findings,
# # # # # # # retrieved evidence, and human feedback.

# # # # # # # IMPORTANT REPORT GENERATION RULES:

# # # # # # # 1. The report structure MUST adapt dynamically
# # # # # # # based on:
# # # # # # # - research query
# # # # # # # - available findings
# # # # # # # - domain context
# # # # # # # - technical depth
# # # # # # # - retrieved evidence
# # # # # # # - human feedback and refinement instructions

# # # # # # # 2. ONLY include sections that are:
# # # # # # # - relevant
# # # # # # # - meaningful
# # # # # # # - evidence-backed
# # # # # # # - contextually useful

# # # # # # # 3. DO NOT generate:
# # # # # # # - empty sections
# # # # # # # - placeholder text
# # # # # # # - irrelevant headings
# # # # # # # - generic filler content

# # # # # # # 4. NEVER include phrases like:
# # # # # # # - "No information available"
# # # # # # # - "Data unavailable"
# # # # # # # - "Insufficient information"

# # # # # # # 5. If a topic lacks sufficient evidence,
# # # # # # # omit that section naturally.

# # # # # # # 6. The report should:
# # # # # # # - feel natural
# # # # # # # - feel professionally written
# # # # # # # - avoid rigid templating
# # # # # # # - maintain strong narrative flow

# # # # # # # 7. Prioritize:
# # # # # # # - technical depth
# # # # # # # - analytical reasoning
# # # # # # # - evidence-backed conclusions
# # # # # # # - real-world implications
# # # # # # # - contextual relevance
# # # # # # # - professional readability

# # # # # # # 8. Adapt section names dynamically
# # # # # # # when appropriate.

# # # # # # # Examples:
# # # # # # # - AI queries may include:
# # # # # # #   - Ethical Considerations
# # # # # # #   - Industry Adoption
# # # # # # #   - Technical Innovations

# # # # # # # - Healthcare queries may include:
# # # # # # #   - Clinical Applications
# # # # # # #   - Patient Impact
# # # # # # #   - Regulatory Challenges

# # # # # # # - Education queries may include:
# # # # # # #   - Personalized Learning
# # # # # # #   - Student Outcomes
# # # # # # #   - Learning Analytics

# # # # # # # - Blockchain queries may include:
# # # # # # #   - Smart Contract Security
# # # # # # #   - Decentralization
# # # # # # #   - Consensus Mechanisms

# # # # # # # 9. Every included section should contain:
# # # # # # # - meaningful explanations
# # # # # # # - technical insights
# # # # # # # - detailed analysis
# # # # # # # - professional formatting
# # # # # # # - strong logical flow

# # # # # # # 10. Avoid:
# # # # # # # - repetitive statements
# # # # # # # - shallow summaries
# # # # # # # - unnecessary verbosity
# # # # # # # - unsupported claims

# # # # # # # 11. Human feedback MUST be incorporated carefully
# # # # # # # to refine:
# # # # # # # - report focus
# # # # # # # - analysis direction
# # # # # # # - emphasis areas
# # # # # # # - technical depth
# # # # # # # - report customization

# # # # # # # RESEARCH QUERY:
# # # # # # # {query}

# # # # # # # KEY FINDINGS:
# # # # # # # {findings}


# # # # # # # Dynamic Sections:
# # # # # # # {dynamic_sections}

# # # # # # # CITATIONS:
# # # # # # # {citations}

# # # # # # # HUMAN FEEDBACK:
# # # # # # # {human_feedback}
# # # # # # # Every dynamic section MUST preserve citations
# # # # # # # from the analysis.

# # # # # # # Each section should include:

# # # # # # # - content
# # # # # # # - evidence attribution
# # # # # # # - supporting URLs

# # # # # # # Generate a polished,
# # # # # # # publication-quality,
# # # # # # # query-adaptive research report
# # # # # # # that dynamically adapts to:
# # # # # # # - the query
# # # # # # # - retrieved evidence
# # # # # # # - available findings
# # # # # # # - human feedback
# # # # # # # - research depth
# # # # # # # - domain context.
# # # # # # # Return report using EXACTLY
# # # # # # # these fields:

# # # # # # # {{
# # # # # # #   "title": "...",
# # # # # # #   "abstract": "...",
# # # # # # #   "keywords": [],
# # # # # # #   "introduction": "...",
# # # # # # #   "methodology": "...",
# # # # # # #   "dynamic_sections": [
# # # # # # #     {{
# # # # # # #       "heading": "...",
# # # # # # #       "content": "...",
# # # # # # #       "citations":"..."
# # # # # # #     }}
# # # # # # #   ],
# # # # # # #   "conclusion": "...",
# # # # # # #   "references": []
# # # # # # # }}

# # # # # # # Return VALID JSON ONLY.
# # # # # # # Do not generate markdown.
# # # # # # # Do not generate extra fields.
# # # # # # # """
# # # # # # REPORT_PROMPT = """

# # # # # # You are an expert Research Report
# # # # # # Generation Agent.

# # # # # # CURRENT DATE:
# # # # # # {current_date}

# # # # # # Generate a professional,
# # # # # # evidence-grounded,
# # # # # # research-paper-style report.

# # # # # # RESEARCH QUERY:
# # # # # # {query}

# # # # # # KEY FINDINGS:
# # # # # # {findings}

# # # # # # DYNAMIC SECTIONS:
# # # # # # {dynamic_sections}

# # # # # # CITATIONS:
# # # # # # {citations}

# # # # # # HUMAN FEEDBACK:
# # # # # # {human_feedback}

# # # # # # IMPORTANT RULES:

# # # # # # 1. Preserve ALL provided dynamic sections.

# # # # # # 2. Do NOT regenerate unrelated sections.

# # # # # # 3. Maintain professional academic tone.

# # # # # # 4. Avoid:
# # # # # # - markdown
# # # # # # - placeholder text
# # # # # # - unsupported claims
# # # # # # - repetitive explanations

# # # # # # 5. Every dynamic section must preserve:
# # # # # # - heading
# # # # # # - content
# # # # # # - citations

# # # # # # 6. Return VALID JSON ONLY.

# # # # # # 7. Do NOT generate extra fields.

# # # # # # Return EXACTLY this schema:

# # # # # # {
# # # # # #   "title": "...",
# # # # # #   "abstract": "...",
# # # # # #   "keywords": [],
# # # # # #   "introduction": "...",
# # # # # #   "methodology": "...",
# # # # # #   "dynamic_sections": [
# # # # # #     {
# # # # # #       "heading": "...",
# # # # # #       "content": "...",
# # # # # #       "citations": []
# # # # # #     }
# # # # # #   ],
# # # # # #   "conclusion": "...",
# # # # # #   "references": []
# # # # # # }

# # # # # # """
# # # # # from datetime import (
# # # # #     datetime
# # # # # )

# # # # # from models.llm_registry import (
# # # # #     report_llm
# # # # # )

# # # # # from prompts.reporting import (
# # # # #     REPORT_PROMPT
# # # # # )

# # # # # from schemas.output import (
# # # # #     ReportOutput
# # # # # )

# # # # # import json
# # # # # import traceback


# # # # # def reporting_agent(state):

# # # # #     print("Report agent")

# # # # #     # --------------------------------
# # # # #     # ANALYSIS
# # # # #     # --------------------------------

# # # # #     analysis = state.get(
# # # # #         "analysis",
# # # # #         {}
# # # # #     )

# # # # #     findings = analysis.get(
# # # # #         "key_findings",
# # # # #         []
# # # # #     )

# # # # #     dynamic_sections = analysis.get(
# # # # #         "dynamic_sections",
# # # # #         []
# # # # #     )

# # # # #     # =====================================
# # # # #     # SECTION OPERATION
# # # # #     # =====================================

# # # # #     section_operation = state.get(
# # # # #         "section_operation",
# # # # #         {}
# # # # #     )

# # # # #     operation = section_operation.get(
# # # # #         "operation",
# # # # #         "none"
# # # # #     )

# # # # #     target_section = section_operation.get(
# # # # #         "target_section",
# # # # #         ""
# # # # #     ).strip().lower()

# # # # #     # =====================================
# # # # #     # DELETE SECTION
# # # # #     # =====================================

# # # # #     if operation == "delete":

# # # # #         filtered_sections = []

# # # # #         for section in dynamic_sections:

# # # # #             heading = section.get(
# # # # #                 "heading",
# # # # #                 ""
# # # # #             ).strip().lower()

# # # # #             if heading != target_section:

# # # # #                 filtered_sections.append(
# # # # #                     section
# # # # #                 )

# # # # #         analysis[
# # # # #             "dynamic_sections"
# # # # #         ] = filtered_sections

# # # # #         dynamic_sections = filtered_sections

# # # # #     # =====================================
# # # # #     # CITATIONS
# # # # #     # =====================================

# # # # #     citations = []

# # # # #     for section in dynamic_sections:

# # # # #         section_citations = section.get(
# # # # #             "citations",
# # # # #             []
# # # # #         )

# # # # #         for citation in section_citations:

# # # # #             if citation not in citations:

# # # # #                 citations.append(
# # # # #                     citation
# # # # #                 )

# # # # #     print(
# # # # #         f"\nCitations Count: "
# # # # #         f"{len(citations)}"
# # # # #     )

# # # # #     # =====================================
# # # # #     # CURRENT DATE
# # # # #     # =====================================

# # # # #     current_date = datetime.now().strftime(
# # # # #         "%d-%m-%Y"
# # # # #     )

# # # # #     # =====================================
# # # # #     # QUERY
# # # # #     # =====================================

# # # # #     query = state.get(
# # # # #         "query",
# # # # #         ""
# # # # #     )

# # # # #     human_feedback = state.get(
# # # # #         "human_feedback",
# # # # #         ""
# # # # #     )

# # # # #     # =====================================
# # # # #     # LIMIT SECTION SIZE
# # # # #     # =====================================

# # # # #     trimmed_sections = []

# # # # #     for section in dynamic_sections:

# # # # #         trimmed_sections.append({

# # # # #             "heading":
# # # # #                 section.get(
# # # # #                     "heading",
# # # # #                     ""
# # # # #                 ),

# # # # #             "content":
# # # # #                 section.get(
# # # # #                     "content",
# # # # #                     ""
# # # # #                 )[:3000],

# # # # #             "citations":
# # # # #                 section.get(
# # # # #                     "citations",
# # # # #                     []
# # # # #                 )[:10]
# # # # #         })

# # # # #     # =====================================
# # # # #     # PROMPT
# # # # #     # =====================================

# # # # #     prompt = REPORT_PROMPT.format(

# # # # #         current_date=current_date,

# # # # #         query=query,

# # # # #         findings=findings,

# # # # #         dynamic_sections=
# # # # #             trimmed_sections,

# # # # #         citations=citations,

# # # # #         human_feedback=
# # # # #             human_feedback
# # # # #     )

# # # # #     # =====================================
# # # # #     # GENERATE REPORT
# # # # #     # =====================================

# # # # #     try:

# # # # #         raw_response = report_llm.invoke(
# # # # #             prompt
# # # # #         )

# # # # #         print(
# # # # #             "\n========== RAW REPORT ==========\n"
# # # # #         )

# # # # #         print(raw_response.content)

# # # # #         cleaned = raw_response.content.strip()

# # # # #         cleaned = cleaned.replace(
# # # # #             "```json",
# # # # #             ""
# # # # #         )

# # # # #         cleaned = cleaned.replace(
# # # # #             "```",
# # # # #             ""
# # # # #         ).strip()

# # # # #         parsed = json.loads(
# # # # #             cleaned
# # # # #         )

# # # # #         report = ReportOutput(
# # # # #             **parsed
# # # # #         ).model_dump()

# # # # #         # =====================================
# # # # #         # PRESERVE FULL SECTIONS
# # # # #         # =====================================

# # # # #         report[
# # # # #             "dynamic_sections"
# # # # #         ] = dynamic_sections

# # # # #     except Exception as e:

# # # # #         print(
# # # # #             "\n========== REPORT ERROR ==========\n"
# # # # #         )

# # # # #         traceback.print_exc()

# # # # #         return {

# # # # #             "critical_error": True,

# # # # #             "errors": [
# # # # #                 str(e)
# # # # #             ],

# # # # #             "workflow_complete":
# # # # #                 True,

# # # # #             "next_agent":
# # # # #                 "FINISH"
# # # # #         }

# # # # #     # =====================================
# # # # #     # RETURN
# # # # #     # =====================================

# # # # #     return {

# # # # #         "analysis":
# # # # #             analysis,

# # # # #         "report":
# # # # #             report,

# # # # #         "workflow_complete":
# # # # #             True,

# # # # #         "next_agent":
# # # # #             "FINISH"
# # # # #     }
# # # # from datetime import datetime
# # # # from models.llm_registry import report_llm
# # # # from prompts.reporting import REPORT_PROMPT
# # # # from schemas.output import ReportOutput

# # # # import json
# # # # import traceback


# # # # def reporting_agent(state):

# # # #     print("Report agent started")

# # # #     try:

# # # #         # =====================================
# # # #         # ANALYSIS
# # # #         # =====================================

# # # #         analysis = state.get(
# # # #             "analysis",
# # # #             {}
# # # #         )

# # # #         findings = analysis.get(
# # # #             "key_findings",
# # # #             []
# # # #         )

# # # #         dynamic_sections = analysis.get(
# # # #             "dynamic_sections",
# # # #             []
# # # #         )

# # # #         # =====================================
# # # #         # LIMIT FINDINGS
# # # #         # =====================================

# # # #         findings = findings[:10]

# # # #         # =====================================
# # # #         # LIMIT DYNAMIC SECTIONS
# # # #         # =====================================

# # # #         trimmed_sections = []

# # # #         for section in dynamic_sections[:5]:

# # # #             trimmed_sections.append({

# # # #                 "heading":
# # # #                     str(
# # # #                         section.get(
# # # #                             "heading",
# # # #                             ""
# # # #                         )
# # # #                     )[:200],

# # # #                 "content":
# # # #                     str(
# # # #                         section.get(
# # # #                             "content",
# # # #                             ""
# # # #                         )
# # # #                     )[:1200],

# # # #                 "citations":
# # # #                     section.get(
# # # #                         "citations",
# # # #                         []
# # # #                     )[:5]
# # # #             })

# # # #         # =====================================
# # # #         # CURRENT DATE
# # # #         # =====================================

# # # #         current_date = datetime.now().strftime(
# # # #             "%d-%m-%Y"
# # # #         )

# # # #         # =====================================
# # # #         # QUERY
# # # #         # =====================================

# # # #         query = str(
# # # #             state.get(
# # # #                 "query",
# # # #                 ""
# # # #             )
# # # #         )[:1000]

# # # #         human_feedback = str(
# # # #             state.get(
# # # #                 "human_feedback",
# # # #                 ""
# # # #             )
# # # #         )[:1000]

# # # #         # =====================================
# # # #         # PROMPT
# # # #         # =====================================

# # # #         prompt = REPORT_PROMPT.format(

# # # #             current_date=current_date,

# # # #             query=query,

# # # #             findings=json.dumps(
# # # #                 findings
# # # #             ),

# # # #             dynamic_sections=json.dumps(
# # # #                 trimmed_sections
# # # #             ),

# # # #             citations="[]",

# # # #             human_feedback=human_feedback
# # # #         )

# # # #         print("Prompt created")

# # # #         print(
# # # #             f"Prompt Length: {len(prompt)}"
# # # #         )

# # # #         # =====================================
# # # #         # RAW INVOKE
# # # #         # =====================================

# # # #         raw_response = report_llm.invoke(
# # # #             prompt
# # # #         )

# # # #         print("LLM CALL SUCCESS")

# # # #         content = raw_response.content

# # # #         print(content)

# # # #         # =====================================
# # # #         # CLEAN JSON
# # # #         # =====================================

# # # #         cleaned = content.strip()

# # # #         cleaned = cleaned.replace(
# # # #             "```json",
# # # #             ""
# # # #         )

# # # #         cleaned = cleaned.replace(
# # # #             "```",
# # # #             ""
# # # #         ).strip()

# # # #         parsed = json.loads(
# # # #             cleaned
# # # #         )

# # # #         report = ReportOutput(
# # # #             **parsed
# # # #         ).model_dump()

# # # #         # =====================================
# # # #         # PRESERVE ORIGINAL SECTIONS
# # # #         # =====================================

# # # #         report[
# # # #             "dynamic_sections"
# # # #         ] = dynamic_sections

# # # #         return {

# # # #             "analysis":
# # # #                 analysis,

# # # #             "report":
# # # #                 report,

# # # #             "workflow_complete":
# # # #                 True,

# # # #             "next_agent":
# # # #                 "FINISH"
# # # #         }

# # # #     except Exception as e:

# # # #         print(
# # # #             "\n========== REPORT ERROR ==========\n"
# # # #         )

# # # #         traceback.print_exc()

# # # #         return {

# # # #             "critical_error":
# # # #                 True,

# # # #             "errors": [
# # # #                 str(e)
# # # #             ],

# # # #             "workflow_complete":
# # # #                 True,

# # # #             "next_agent":
# # # #                 "FINISH"
# # # #         }

# # # from datetime import datetime

# # # from models.llm_registry import (
# # #     report_llm
# # # )

# # # from prompts.reporting import (
# # #     REPORT_PROMPT
# # # )

# # # from schemas.output import (
# # #     ReportOutput
# # # )

# # # import json
# # # import traceback


# # # def reporting_agent(state):

# # #     print("\n========== REPORT AGENT ==========\n")

# # #     try:

# # #         # =====================================
# # #         # ANALYSIS
# # #         # =====================================

# # #         analysis = state.get(
# # #             "analysis",
# # #             {}
# # #         )
# # #         previous_analysis = state.get(
# # #             "previous_analysis",
# # #             {}
# # #         ) or {}

# # #         previous_report = state.get(
# # #             "previous_report",
# # #             {}
# # #         ) or {}

# # #         findings = analysis.get(
# # #             "key_findings",
# # #             []
# # #         )

# # #         dynamic_sections = (

# # #     analysis.get(
# # #         "dynamic_sections"
# # #     )

# # #     or previous_analysis.get(
# # #         "dynamic_sections",
# # #         []
# # #     )

# # #     or previous_report.get(
# # #         "dynamic_sections",
# # #         []
# # #     )
# # # )

# # #         # =====================================
# # #         # SECTION OPERATION
# # #         # =====================================

# # #         section_operation = state.get(
# # #             "section_operation",
# # #             {}
# # #         )

# # #         operation = section_operation.get(
# # #             "operation",
# # #             "none"
# # #         )

# # #         target_section = section_operation.get(
# # #             "target_section",
# # #             ""
# # #         ).strip().lower()

# # #         if operation == "delete":

# # #             print(
# # #                 "\n========== DELETE OPERATION ==========\n"
# # #             )

# # #             previous_sections = (

# # #                 previous_report.get(
# # #                     "dynamic_sections",
# # #                     []
# # #                 )

# # #                 or previous_analysis.get(
# # #                     "dynamic_sections",
# # #                     []
# # #                 )

# # #                 or analysis.get(
# # #                     "dynamic_sections",
# # #                     []
# # #                 )
# # #             )

# # #             filtered_sections = []

# # #             for section in previous_sections:

# # #                 heading = str(
# # #                     section.get(
# # #                         "heading",
# # #                         ""
# # #                     )
# # #                 ).strip().lower()

# # #                 if heading != target_section:

# # #                     filtered_sections.append(
# # #                         section
# # #                     )

# # #             # =====================================
# # #             # UPDATE WORKING ANALYSIS
# # #             # =====================================

# # #             analysis["dynamic_sections"] = (
# # #                 filtered_sections
# # #             )

# # #             dynamic_sections = (
# # #                 filtered_sections
# # #             )

# # #             print(
# # #                 f"Deleted section: {target_section}"
# # #             )
# # #         # =====================================
# # #         # LIMIT FINDINGS
# # #         # =====================================

# # #         findings = findings[:10]

# # #         # =====================================
# # #         # LIMIT DYNAMIC SECTIONS
# # #         # =====================================

# # #         trimmed_sections = []

# # #         for section in dynamic_sections[:5]:

# # #             trimmed_sections.append({

# # #                 "heading":
# # #                     str(
# # #                         section.get(
# # #                             "heading",
# # #                             ""
# # #                         )
# # #                     )[:200],

# # #                 "content":
# # #                     str(
# # #                         section.get(
# # #                             "content",
# # #                             ""
# # #                         )
# # #                     )[:1200],

# # #                 "citations":
# # #                     section.get(
# # #                         "citations",
# # #                         []
# # #                     )[:5]
# # #             })

# # #         # =====================================
# # #         # CURRENT DATE
# # #         # =====================================

# # #         current_date = datetime.now().strftime(
# # #             "%d-%m-%Y"
# # #         )

# # #         # =====================================
# # #         # QUERY
# # #         # =====================================

# # #         query = str(
# # #             state.get(
# # #                 "query",
# # #                 ""
# # #             )
# # #         )[:1000]

# # #         human_feedback = str(
# # #             state.get(
# # #                 "human_feedback",
# # #                 ""
# # #             )
# # #         )[:1000]

# # #         # =====================================
# # #         # CITATIONS
# # #         # =====================================

# # #         citations = []

# # #         for section in trimmed_sections:

# # #             for citation in section.get(
# # #                 "citations",
# # #                 []
# # #             ):

# # #                 if citation not in citations:

# # #                     citations.append(
# # #                         citation
# # #                     )

# # #         # =====================================
# # #         # PROMPT
# # #         # =====================================

# # #         prompt = REPORT_PROMPT.format(

# # #             current_date=current_date,

# # #             query=query,

# # #             findings=findings,

# # #             dynamic_sections=
# # #                 trimmed_sections,

# # #             citations=citations,

# # #             human_feedback=
# # #                 human_feedback
# # #         )

# # #         print(
# # #             "\n========== PROMPT LENGTH ==========\n"
# # #         )

# # #         print(len(prompt))

# # #         # =====================================
# # #         # RAW INVOKE
# # #         # =====================================

# # #         raw_response = report_llm.invoke(
# # #             prompt
# # #         )

# # #         print(
# # #             "\n========== LLM CALL SUCCESS ==========\n"
# # #         )

# # #         print(type(raw_response))

# # #         print(raw_response)

# # #         # =====================================
# # #         # SAFE CONTENT EXTRACTION
# # #         # =====================================

# # #         content = ""

# # #         if hasattr(
# # #             raw_response,
# # #             "content"
# # #         ):

# # #             if isinstance(
# # #                 raw_response.content,
# # #                 str
# # #             ):

# # #                 content = raw_response.content

# # #             elif isinstance(
# # #                 raw_response.content,
# # #                 list
# # #             ):

# # #                 for item in raw_response.content:

# # #                     if isinstance(
# # #                         item,
# # #                         dict
# # #                     ):

# # #                         content += item.get(
# # #                             "text",
# # #                             ""
# # #                         )

# # #                     else:

# # #                         content += str(item)

# # #             else:

# # #                 content = str(
# # #                     raw_response.content
# # #                 )

# # #         else:

# # #             content = str(
# # #                 raw_response
# # #             )

# # #         print(
# # #             "\n========== EXTRACTED CONTENT ==========\n"
# # #         )

# # #         print(content)

# # #         # =====================================
# # #         # EMPTY RESPONSE CHECK
# # #         # =====================================

# # #         if not content.strip():

# # #             raise ValueError(
# # #                 "Empty response from LLM"
# # #             )

# # #         # =====================================
# # #         # CLEAN JSON
# # #         # =====================================

# # #         cleaned = content.strip()

# # #         cleaned = cleaned.replace(
# # #             "```json",
# # #             ""
# # #         )

# # #         cleaned = cleaned.replace(
# # #             "```",
# # #             ""
# # #         ).strip()

# # #         print(
# # #             "\n========== CLEANED RESPONSE ==========\n"
# # #         )

# # #         print(cleaned)

# # #         # =====================================
# # #         # PARSE JSON
# # #         # =====================================

# # #         parsed = json.loads(
# # #             cleaned
# # #         )

# # #         # =====================================
# # #         # VALIDATE OUTPUT
# # #         # =====================================

# # #         report = ReportOutput(
# # #             **parsed
# # #         ).model_dump()

# # #         # =====================================
# # #         # PRESERVE ORIGINAL SECTIONS
# # #         # =====================================

# # #         report[
# # #             "dynamic_sections"
# # #         ] = dynamic_sections

# # #         print(
# # #             "\n========== REPORT SUCCESS ==========\n"
# # #         )

# # #         # =====================================
# # #         # RETURN
# # #         # =====================================

# # #         return {

# # #             "analysis":
# # #                 analysis,

# # #             "report":
# # #                 report,

# # #             "workflow_complete":
# # #                 True,

# # #             "next_agent":
# # #                 "END"
# # #         }

# # #     except Exception as e:

# # #         print(
# # #             "\n========== REPORT ERROR ==========\n"
# # #         )

# # #         traceback.print_exc()

# # #         return {

# # #             "critical_error":
# # #                 True,

# # #             "errors": [
# # #                 str(e)
# # #             ],

# # #             "workflow_complete":
# # #                 True,

# # #             "next_agent":
# # #                 "FINISH"
# # #         }


# # from datetime import datetime

# # from models.llm_registry import (
# #     report_llm
# # )

# # from prompts.reporting import (
# #     REPORT_PROMPT
# # )

# # from schemas.output import (
# #     ReportOutput
# # )

# # import json
# # import traceback
# # import re


# # def reporting_agent(state):

# #     print(
# #         "\n========== REPORT AGENT ==========\n"
# #     )

# #     try:

# #         # =====================================
# #         # ANALYSIS
# #         # =====================================

# #         analysis = state.get(
# #             "analysis",
# #             {}
# #         )

# #         previous_analysis = state.get(
# #             "previous_analysis",
# #             {}
# #         ) or {}

# #         previous_report = state.get(
# #             "previous_report",
# #             {}
# #         ) or {}

# #         findings = analysis.get(
# #             "key_findings",
# #             []
# #         )

# #         dynamic_sections = (

# #             analysis.get(
# #                 "dynamic_sections"
# #             )

# #             or previous_analysis.get(
# #                 "dynamic_sections",
# #                 []
# #             )

# #             or previous_report.get(
# #                 "dynamic_sections",
# #                 []
# #             )
# #         )

# #         # =====================================
# #         # SECTION OPERATION
# #         # =====================================

# #         section_operation = state.get(
# #             "section_operation",
# #             {}
# #         )

# #         operation = section_operation.get(
# #             "operation",
# #             "none"
# #         )

# #         target_section = section_operation.get(
# #             "target_section",
# #             ""
# #         ).strip().lower()

# #         # =====================================
# #         # DELETE SECTION
# #         # =====================================

# #         if operation == "delete":

# #             print(
# #                 "\n========== DELETE OPERATION ==========\n"
# #             )

# #             previous_sections = (

# #                 previous_report.get(
# #                     "dynamic_sections",
# #                     []
# #                 )

# #                 or previous_analysis.get(
# #                     "dynamic_sections",
# #                     []
# #                 )

# #                 or analysis.get(
# #                     "dynamic_sections",
# #                     []
# #                 )
# #             )

# #             filtered_sections = []

# #             for section in previous_sections:

# #                 heading = str(
# #                     section.get(
# #                         "heading",
# #                         ""
# #                     )
# #                 ).strip().lower()

# #                 if heading != target_section:

# #                     filtered_sections.append(
# #                         section
# #                     )

# #             analysis = {

# #                 **analysis,

# #                 "dynamic_sections":
# #                     filtered_sections
# #             }

# #             dynamic_sections = list(
# #                 filtered_sections
# #             )

# #             previous_analysis = {

# #                 **previous_analysis,

# #                 "dynamic_sections":
# #                     filtered_sections
# #             }

# #             previous_report = {

# #                 **previous_report,

# #                 "dynamic_sections":
# #                     filtered_sections
# #             }
# #             print(
# #                 f"Deleted section: {target_section}"
# #             )

# #         # =====================================
# #         # LIMIT FINDINGS
# #         # =====================================

# #         findings = findings[:10]

# #         # =====================================
# #         # LIMIT DYNAMIC SECTIONS
# #         # =====================================

# #         trimmed_sections = []

# #         for section in dynamic_sections[:5]:

# #             trimmed_sections.append({

# #                 "heading":
# #                     str(
# #                         section.get(
# #                             "heading",
# #                             ""
# #                         )
# #                     )[:200],

# #                 "content":
# #                     str(
# #                         section.get(
# #                             "content",
# #                             ""
# #                         )
# #                     )[:1200],

# #                 "citations":
# #                     section.get(
# #                         "citations",
# #                         []
# #                     )[:5]
# #             })

# #         # =====================================
# #         # CURRENT DATE
# #         # =====================================

# #         current_date = datetime.now().strftime(
# #             "%d-%m-%Y"
# #         )

# #         # =====================================
# #         # QUERY
# #         # =====================================

# #         query = str(
# #             state.get(
# #                 "query",
# #                 ""
# #             )
# #         )[:1000]

# #         human_feedback = str(
# #             state.get(
# #                 "human_feedback",
# #                 ""
# #             )
# #         )[:1000]

# #         # =====================================
# #         # CITATIONS
# #         # =====================================

# #         citations = []

# #         for section in trimmed_sections:

# #             for citation in section.get(
# #                 "citations",
# #                 []
# #             ):

# #                 if citation not in citations:

# #                     citations.append(
# #                         citation
# #                     )

# #         # =====================================
# #         # PROMPT
# #         # =====================================

# #         prompt = REPORT_PROMPT.format(

# #             current_date=current_date,

# #             query=query,

# #             findings=json.dumps(
# #                 findings
# #             ),

# #             dynamic_sections=json.dumps(
# #                 trimmed_sections
# #             ),

# #             citations=json.dumps(
# #                 citations
# #             ),

# #             human_feedback=human_feedback
# #         )

# #         print(
# #             "\n========== PROMPT LENGTH ==========\n"
# #         )

# #         print(len(prompt))

# #         # =====================================
# #         # RAW LLM INVOKE
# #         # =====================================

# #         raw_response = report_llm.invoke(
# #             prompt
# #         )

# #         print(
# #             "\n========== LLM RESPONSE ==========\n"
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
# #             "\n========== RAW CONTENT ==========\n"
# #         )

# #         print(content)

# #         # =====================================
# #         # EMPTY RESPONSE CHECK
# #         # =====================================

# #         if not content.strip():

# #             raise ValueError(
# #                 "Empty response from LLM"
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
# #         # EXTRACT JSON ONLY
# #         # =====================================

# #         json_match = re.search(

# #             r'\{.*\}',

# #             cleaned,

# #             re.DOTALL
# #         )

# #         if not json_match:

# #             raise ValueError(
# #                 "No valid JSON found in LLM response"
# #             )

# #         json_text = json_match.group(0)

# #         print(
# #             "\n========== EXTRACTED JSON ==========\n"
# #         )

# #         print(json_text)

# #         # =====================================
# #         # PARSE JSON
# #         # =====================================

# #         parsed = json.loads(
# #             json_text
# #         )

# #         # =====================================
# #         # VALIDATE OUTPUT
# #         # =====================================

# #         report = ReportOutput(
# #             **parsed
# #         ).model_dump()

# #         # =====================================
# #         # PRESERVE ORIGINAL SECTIONS
# #         # =====================================

# #         # =====================================
# #         # FORCE FINAL FILTERED SECTIONS
# #         # =====================================

# #         if operation == "delete":

# #             report[
# #                 "dynamic_sections"
# #             ] = filtered_sections

# #         else:

# #             report[
# #                 "dynamic_sections"
# #             ] = dynamic_sections

# #         print(
# #             "\n========== REPORT SUCCESS ==========\n"
# #         )

# #         # =====================================
# #         # RETURN SUCCESS
# #         # =====================================

# #         return {

# #             "analysis":
# #                 analysis,

# #             "report":
# #                 report,

# #             "workflow_complete":
# #                 True,

# #             "next_agent":
# #                 "END"
# #         }

# #     except Exception as e:

# #         print(
# #             "\n========== REPORT ERROR ==========\n"
# #         )

# #         traceback.print_exc()

# #         return {

# #             "critical_error": True,

# #             "workflow_complete": True,

# #             "next_agent": "FINISH",

# #             "error": {

# #                 "type": type(e).__name__,

# #                 "message": str(e),

# #                 "raw": traceback.format_exc()
# #             }
# #         }

# from datetime import datetime

# from models.llm_registry import (
#     report_llm
# )

# from prompts.reporting import (
#     REPORT_PROMPT
# )

# from schemas.output import (
#     ReportOutput
# )

# import json
# import traceback
# import re


# def reporting_agent(state):

#     print(
#         "\n========== REPORT AGENT ==========\n"
#     )

#     try:

#         # =====================================
#         # ANALYSIS
#         # =====================================

#         analysis = state.get(
#             "analysis",
#             {}
#         )

#         previous_analysis = state.get(
#             "previous_analysis",
#             {}
#         ) or {}

#         previous_report = state.get(
#             "previous_report",
#             {}
#         ) or {}

#         findings = analysis.get(
#             "key_findings",
#             []
#         )

#         # =====================================
#         # LOAD DYNAMIC SECTIONS SAFELY
#         # =====================================

#         dynamic_sections = analysis.get(
#             "dynamic_sections",
#             None
#         )

#         print(
#             "\n[DEBUG] analysis dynamic_sections"
#         )

#         print(dynamic_sections)

#         if dynamic_sections is None:

#             dynamic_sections = previous_analysis.get(
#                 "dynamic_sections",
#                 None
#             )

#             print(
#                 "\n[DEBUG] loaded from previous_analysis"
#             )

#             print(dynamic_sections)

#         if dynamic_sections is None:

#             dynamic_sections = previous_report.get(
#                 "dynamic_sections",
#                 []
#             )

#             print(
#                 "\n[DEBUG] loaded from previous_report"
#             )

#             print(dynamic_sections)

#         print(
#             "\n[DEBUG] FINAL dynamic_sections BEFORE DELETE"
#         )

#         print([
#             section.get("heading")
#             for section in dynamic_sections
#         ])

#         # =====================================
#         # SECTION OPERATION
#         # =====================================

#         section_operation = state.get(
#             "section_operation",
#             {}
#         )

#         operation = section_operation.get(
#             "operation",
#             "none"
#         )

#         target_section = section_operation.get(
#             "target_section",
#             ""
#         ).strip().lower()

#         print("\n[DEBUG] operation")
#         print(operation)

#         print("\n[DEBUG] target_section")
#         print(target_section)

#         # =====================================
#         # DELETE SECTION
#         # =====================================

#         if operation == "delete":

#             print(
#                 "\n========== DELETE OPERATION ==========\n"
#             )

#             filtered_sections = []

#             print(
#                 "\n[DEBUG] Sections BEFORE delete"
#             )

#             for section in dynamic_sections:

#                 print(
#                     section.get("heading")
#                 )

#             for section in dynamic_sections:

#                 heading = str(
#                     section.get(
#                         "heading",
#                         ""
#                     )
#                 ).strip().lower()

#                 print("\n[DEBUG] Comparing")
#                 print(f"Current: {heading}")
#                 print(f"Target : {target_section}")

#                 if heading != target_section:

#                     filtered_sections.append(
#                         section
#                     )

#                 else:

#                     print(
#                         f"\n[DEBUG] DELETED => {heading}"
#                     )

#             print(
#                 "\n[DEBUG] Sections AFTER delete"
#             )

#             for section in filtered_sections:

#                 print(
#                     section.get("heading")
#                 )

#             # =====================================
#             # FORCE UPDATE EVERYWHERE
#             # =====================================

#             analysis["dynamic_sections"] = (
#                 filtered_sections
#             )

#             previous_analysis["dynamic_sections"] = (
#                 filtered_sections
#             )

#             previous_report["dynamic_sections"] = (
#                 filtered_sections
#             )

#             dynamic_sections = filtered_sections

#             print(
#                 "\n[DEBUG] FINAL STORED dynamic_sections"
#             )

#             print([
#                 section.get("heading")
#                 for section in dynamic_sections
#             ])

#         # =====================================
#         # LIMIT FINDINGS
#         # =====================================

#         findings = findings[:10]

#         # =====================================
#         # LIMIT DYNAMIC SECTIONS
#         # =====================================

#         trimmed_sections = []

#         for section in dynamic_sections[:5]:

#             trimmed_sections.append({

#                 "heading":
#                     str(
#                         section.get(
#                             "heading",
#                             ""
#                         )
#                     )[:200],

#                 "content":
#                     str(
#                         section.get(
#                             "content",
#                             ""
#                         )
#                     )[:1200],

#                 "citations":
#                     section.get(
#                         "citations",
#                         []
#                     )[:5]
#             })

#         print(
#             "\n[DEBUG] trimmed_sections"
#         )

#         print([
#             section.get("heading")
#             for section in trimmed_sections
#         ])

#         # =====================================
#         # CURRENT DATE
#         # =====================================

#         current_date = datetime.now().strftime(
#             "%d-%m-%Y"
#         )

#         # =====================================
#         # QUERY
#         # =====================================

#         query = str(
#             state.get(
#                 "query",
#                 ""
#             )
#         )[:1000]

#         human_feedback = str(
#             state.get(
#                 "human_feedback",
#                 ""
#             )
#         )[:1000]

#         # =====================================
#         # CITATIONS
#         # =====================================

#         citations = []

#         for section in trimmed_sections:

#             for citation in section.get(
#                 "citations",
#                 []
#             ):

#                 if citation not in citations:

#                     citations.append(
#                         citation
#                     )

#         # =====================================
#         # PROMPT
#         # =====================================

#         prompt = REPORT_PROMPT.format(

#             current_date=current_date,

#             query=query,

#             findings=json.dumps(
#                 findings
#             ),

#             dynamic_sections=json.dumps(
#                 trimmed_sections
#             ),

#             citations=json.dumps(
#                 citations
#             ),

#             human_feedback=human_feedback
#         )

#         print(
#             "\n========== PROMPT LENGTH ==========\n"
#         )

#         print(len(prompt))

#         print(
#             "\n========== FINAL SECTIONS SENT TO LLM ==========\n"
#         )

#         print([
#             section.get("heading")
#             for section in trimmed_sections
#         ])

#         # =====================================
#         # RAW LLM INVOKE
#         # =====================================

#         raw_response = report_llm.invoke(
#             prompt
#         )

#         print(
#             "\n========== LLM RESPONSE ==========\n"
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
#             "\n========== RAW CONTENT ==========\n"
#         )

#         print(content)

#         # =====================================
#         # EMPTY RESPONSE CHECK
#         # =====================================

#         if not content.strip():

#             raise ValueError(
#                 "Empty response from LLM"
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
#         # EXTRACT JSON ONLY
#         # =====================================

#         json_match = re.search(

#             r'\{.*\}',

#             cleaned,

#             re.DOTALL
#         )

#         if not json_match:

#             raise ValueError(
#                 "No valid JSON found in LLM response"
#             )

#         json_text = json_match.group(0)

#         print(
#             "\n========== EXTRACTED JSON ==========\n"
#         )

#         print(json_text)

#         # =====================================
#         # PARSE JSON
#         # =====================================

#         parsed = json.loads(
#             json_text
#         )

#         # =====================================
#         # VALIDATE OUTPUT
#         # =====================================

#         report = ReportOutput(
#             **parsed
#         ).model_dump()

#         # =====================================
#         # FORCE FINAL FILTERED SECTIONS
#         # =====================================

#         report[
#             "dynamic_sections"
#         ] = dynamic_sections

#         print(
#             "\n========== FINAL REPORT SECTIONS ==========\n"
#         )

#         print([
#             section.get("heading")
#             for section in report[
#                 "dynamic_sections"
#             ]
#         ])

#         print(
#             "\n========== REPORT SUCCESS ==========\n"
#         )

#         # =====================================
#         # RETURN SUCCESS
#         # =====================================

#         return {

#             "analysis":
#                 analysis,

#             "previous_analysis":
#                 previous_analysis,

#             "previous_report":
#                 previous_report,

#             "report":
#                 report,

#             "workflow_complete":
#                 True,

#             "next_agent":
#                 "END"
#         }

#     except Exception as e:

#         print(
#             "\n========== REPORT ERROR ==========\n"
#         )

#         traceback.print_exc()

#         return {

#             "critical_error": True,

#             "workflow_complete": True,

#             "next_agent": "FINISH",

#             "error": {

#                 "type": type(e).__name__,

#                 "message": str(e),

#                 "raw": traceback.format_exc()
#             }
#         }
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

    except Exception as e:

        print(
            "\n========== REPORT ERROR ==========\n"
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