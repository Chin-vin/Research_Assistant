
import os
import base64
import traceback
from dotenv import load_dotenv
from models.llm_registry import reasoning_llm,fast_llm
load_dotenv()
os.environ["STREAMLIT_SERVER_FILE_WATCHER_TYPE"] = "none"
from utils.report_chat import (
    chat_with_report
)
from rag.retriever import retrieve_documents
import streamlit as st
import warnings
from rag.vectorstore import (
    cleanup_all_vectorstores,
    delete_vectorstore
)

warnings.filterwarnings("ignore")

from session_manager import SessionManager
from workflow.graph import graph
from utils.pdf_generator import generate_pdf_report
from utils.file_handler import save_uploaded_file
from rag.loader import load_pdf
from rag.splitter import split_documents
from rag.vectorstore import create_vectorstore

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Intelligent Research Assistant",
    page_icon="📘",
    layout="wide",
)

st.markdown("""
<style>

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 1rem;
    max-width: 95%;
}

h1, h2, h3 {
    font-weight: 650 !important;
}

div[data-testid="stChatMessage"] {
    padding: 0.8rem 1rem;
    border-radius: 12px;
    margin-bottom: 0.8rem;
    border: 1px solid rgba(120,120,120,0.15);
}

.stButton > button {
    border-radius: 10px;
    font-weight: 600;
}

.stTextArea textarea {
    border-radius: 10px !important;
}

button[data-baseweb="tab"] {
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-weight: 500;
}

</style>
""", unsafe_allow_html=True)


if "uploader_reset_counter" not in st.session_state:
    st.session_state["uploader_reset_counter"] = 0

# =========================================================
# ERROR CLASSIFICATION
# =========================================================
def classify_error(error_payload):

    print("\n" + "=" * 100)
    print("CLASSIFY_ERROR")
    print("=" * 100)

    print("PAYLOAD:")
    print(error_payload)

    print("=" * 100 + "\n")

    error_type = error_payload.get(
        "type",
        "UnknownError"
    )

    error_message = error_payload.get(
        "message",
        ""
    )
    combined = f"""

{error_type}

{error_message}

""".lower()
    error_map = {

        "RateLimitError": (

    "Rate Limit Exceeded",

    (
        "The AI provider rate limit was exceeded.\n\n"

        "Possible reasons:\n"

        "- Too many requests\n"
        "- Daily quota exhausted\n"
        "- Tokens per minute exceeded\n"
        "- Temporary provider overload\n\n"

        "Please wait a few minutes and retry."
    )
),

        "Timeout": (

            "Connection timeout",

            (
                "The request timed out while "
                "reaching the AI model."
            )
        ),

        "ValidationError": (

            "Structured response validation failed",

            (
                "The AI model returned an "
                "invalid structured response."
            )
        ),

        "JSONDecodeError": (

            "Malformed JSON response",

            (
                "The AI model returned "
                "invalid JSON output."
            )
        ),

        "RecursionError": (

            "Workflow recursion exceeded",

            (
                "The workflow exceeded "
                "maximum recursion depth."
            )
        ),

        "KeyError": (

            "Missing workflow state",

            (
                "A required workflow state "
                "value was missing."
            )
        ),


        "AttributeError": (

            "Internal workflow attribute error",

            (
                "An internal workflow object "
                "was invalid."
            )
        )
    }

    # =====================================
    # FALLBACK RATE LIMIT DETECTION
    # =====================================

    if (

    "429" in combined

    or "rate limit" in combined

    or "rate_limit_exceeded"
        in combined

    or "tokens per day"
        in combined

    or "quota exceeded"
        in combined

    or "insufficient quota"
        in combined
):

        return (

            "Rate limit reached",

            (
                "The AI provider temporarily "
                "rejected requests due to "
                "usage limits.\n\n"
                "Please wait a few minutes "
                "and retry."
            )
        )

    return error_map.get(

        error_type,

        (

            "Unexpected workflow error",

            error_message
            if error_message
            else
            "Something went wrong while generating the report."
        )
    )
def save_error_message(error_payload):

    print("\n" + "=" * 100)
    print("SAVE_ERROR_MESSAGE EXECUTED")
    print("=" * 100)

    print("ERROR PAYLOAD:")
    print(error_payload)

    print("=" * 100 + "\n")

    if not isinstance(
        error_payload,
        dict
    ):

        error_payload = {

            "type":
                "UnknownError",

            "message":
                str(error_payload)
        }

    print("\n" + "=" * 100)
    print("ABOUT TO CLASSIFY ERROR")
    print("=" * 100)

    print(error_payload)

    print("=" * 100 + "\n")

    err_title, err_body = classify_error(
        error_payload
    )

    print("\n" + "=" * 100)
    print("CLASSIFY ERROR COMPLETE")
    print("=" * 100)

    print("TITLE:")
    print(err_title)

    print("\nBODY:")
    print(err_body)

    print("=" * 100 + "\n")

    error_message = {

        "_type":
            "workflow_error",

        "title":
            err_title,

        "message":
            err_body,

        "error":
            error_payload
    }

    print("\n" + "=" * 100)
    print("ERROR MESSAGE OBJECT")
    print("=" * 100)

    print(error_message)

    print("=" * 100 + "\n")

    SessionManager.add_message(

        "assistant",

        error_message
    )

    print("\nERROR MESSAGE SAVED\n")
def stream_graph(state, recursion_limit=20):

    events = graph.stream(

        state,

        config={
            "recursion_limit": recursion_limit
        },

        stream_mode="updates",
    )

    merged = state.copy()

    for event in events:

        for node, value in event.items():

            if isinstance(value, dict):

                # =====================================
                # MERGE ANALYSIS SAFELY
                # =====================================

                if "analysis" in value:

                    old_analysis = merged.get(
                        "analysis",
                        {}
                    ) or {}

                    new_analysis = value.get(
                        "analysis",
                        {}
                    ) or {}

                    merged_analysis = old_analysis.copy()

                    for k, v in new_analysis.items():

                        if v in [
                            "",
                            [],
                            {},
                            None
                        ]:
                            continue

                        merged_analysis[k] = v

                    merged[
                        "analysis"
                    ] = merged_analysis

                # =====================================
                # MERGE REPORT SAFELY
                # =====================================

                if "report" in value:

                    old_report = merged.get(
                        "report",
                        {}
                    ) or {}

                    new_report = value.get(
                        "report",
                        {}
                    ) or {}

                    merged_report = old_report.copy()

                    for k, v in new_report.items():

                        if v in [
                            "",
                            [],
                            {},
                            None
                        ]:
                            continue

                        merged_report[k] = v

                    merged[
                        "report"
                    ] = merged_report

                # =====================================
                # NORMAL FIELDS
                # =====================================

                for k, v in value.items():

                    if k not in [
                        "analysis",
                        "report"
                    ]:

                        merged[k] = v

                # =====================================
                # CRITICAL ERROR
                # =====================================

                if value.get(
                    "critical_error"
                ):

                    for _ in events:
                        pass

                    return merged, True

    return merged, False
if "app_initialized" not in st.session_state:

    cleanup_all_vectorstores()

    st.session_state[
        "app_initialized"
    ] = True

SessionManager.initialize()
# =========================================================
# SESSION INITIALIZATION
# =========================================================

# SessionManager.initialize()
current_session = SessionManager.get_current_session()

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.title("Research Assistant")
    st.divider()
    st.subheader("Research Sessions")

    if st.button("New Session", use_container_width=True):
        SessionManager.create_new_session()
        st.rerun()

    st.divider()

    sessions = st.session_state.sessions
    for session_id in list(sessions.keys())[::-1]:
        btn_type = (
            "primary"
            if session_id == st.session_state.current_session_id
            else "secondary"
        )
        if st.button(
            session_id[:8],
            key=session_id,
            use_container_width=True,
            type=btn_type,
        ):
            st.session_state.current_session_id = session_id
            st.rerun()

current_session = SessionManager.get_current_session()

# =========================================================
# HEADER
# =========================================================

# with st.container(border=True):

#     st.title(
#         "Intelligent Research Assistant"
#     )

#     st.caption(
#         "Multi-Agent AI powered research generation, document analysis, validation, and reporting platform."
#     )

# st.divider()
st.title(
        "Intelligent Research Assistant"
    )
st.divider()
# =========================================================
# ALWAYS FETCH LATEST SESSION
# =========================================================

current_session = (
    SessionManager.get_current_session()
)

messages = current_session.get(
    "messages",
    []
)

print("\n========== CHAT HISTORY ==========")

print(
    f"MESSAGE COUNT: {len(messages)}"
)

for i, msg in enumerate(messages):
    print(f"\nMESSAGE {i}")
    print(msg)

print("\n==================================")

if not messages:

    # st.markdown(
    #     "## AI Research Assistant"
    # )

    st.caption(
        "Generate intelligent research reports using "
        "multi-agent retrieval, PDF analysis, "
        "reasoning workflows, validation loops, "
        "and structured report generation."
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(
            "📂 Intelligent Research Input\n\n"

            "- Upload PDFs and research papers\n"
            "- Ask research-related questions\n"
            "- Use hybrid PDF + query workflows\n"
        )

    with col2:

        st.info(

            "🤖 Multi-Agent Pipeline\n"

            "- Query decomposition and routing\n"
            "- Parallel web, arXiv, and PDF retrieval\n"
            "- Deep analytical reasoning and synthesis\n"
        )

    with col3:

        st.info(

            "📑 Validated Research Reports\n\n"

            "- Dynamic section generation\n"
            "- Evidence-backed findings and citations\n"
            "- Validation, refinement, and report generation")

for idx, msg in enumerate(messages):
    print("\n" + "=" * 100)
    print("CHAT MESSAGE RENDER")
    print("=" * 100)

    print("INDEX:")
    print(idx)

    print("\nROLE:")
    print(msg.get("role"))

    print("\nCONTENT TYPE:")
    print(type(msg.get("content")))

    print("\nCONTENT:")
    print(msg.get("content"))

    print("=" * 100 + "\n")

    with st.chat_message(msg["role"]):
        content = msg["content"]

        # --------------------------------------------------
        # CHECK _type FIRST — before any other dict check
        # This must be first because workflow_error dicts
        # also contain a "title" key which would otherwise
        # match the report condition below.
        # --------------------------------------------------
        if (
    isinstance(content, dict)

            and content.get("_type")
                == "workflow_error"
        ):

            print("\n========== RENDERING ERROR ==========")
            print(content)
            print("\n====================================")

            print("\n" + "=" * 100)
            print("RENDERING WORKFLOW ERROR")
            print("=" * 100)

            print("TITLE:")
            print(content.get("title"))

            print("\nMESSAGE:")
            print(content.get("message"))

            print("\nERROR OBJECT:")
            print(content.get("error"))

            print("=" * 100 + "\n")

            st.error(
            
                f"**{content.get('title', 'Workflow Failed')}**"
            )

            st.markdown(
                content.get("message", "")
            )

            error_payload = content.get(
                "error",
                {}
            )

            if error_payload.get(
                "message"
            ):

                st.warning(
                    error_payload["message"]
                )

            st.info(
                "You can start a new query below."
            )

            if error_payload:
            
                with st.expander(
                    "Technical details"
                ):

                    st.code(
                    
                        error_payload.get(
                            "message",
                            ""
                        )
                    )

                    raw = error_payload.get(
                        "raw",
                        ""
                    )

                    if raw:
                    
                        st.code(raw)

        # --------------------------------------------------
        # REPORT MESSAGE
        # --------------------------------------------------
        elif (
            isinstance(content, dict)
            and content.get("title")
            and (content.get("abstract") or content.get("dynamic_sections"))
        ):
            st.subheader(content.get("title", "Research Report"))

            available_tabs = []
            tab_content = {}

            for field, label in [
                ("abstract", "Abstract"),
                ("introduction", "Introduction"),
                ("methodology", "Methodology"),
                ("conclusion", "Conclusion"),
            ]:
                val = content.get(field, "")
                if val:
                    available_tabs.append(label)
                    tab_content[label] = val

            findings = content.get("key_findings", [])
            if findings:
                available_tabs.append("Key Findings")
                tab_content["Key Findings"] = findings

            for section in content.get("dynamic_sections", []):
                heading = section.get("heading", "")
                body = section.get("content", "")
                if heading and body:
                    available_tabs.append(heading)
                    tab_content[heading] = {
                        "content": body,
                        "citations": section.get("citations", []),
                    }

            references = content.get("references", [])
            # =====================================
            # EXTRA REPORT TABS
            # =====================================

            available_tabs.extend([
            
                # "Quick Findings",

                # "Chat With PDF"
            ])
            if references:
                available_tabs.append("References")
                tab_content["References"] = references

            if available_tabs:
                tabs = st.tabs(available_tabs)
                for tab_idx, tab_name in enumerate(available_tabs):
                    with tabs[tab_idx]:
                                        
                        # =====================================
                        # QUICK FINDINGS
                        # =====================================

                        # if tab_name == "Quick Findings":
                        
                        #     findings = content.get(
                        #         "key_findings",
                        #         []
                        #     )

                        #     if findings:
                            
                        #         for item in findings:
                                
                        #             st.markdown(
                        #                 f"- {item}"
                        #             )

                        #     else:
                            
                        #         st.info(
                        #             "No findings available."
                        #         )

                        # =====================================
                        # CHAT WITH PDF
                        # =====================================

                        # elif tab_name == "Chat With PDF":
                        
                        #     report_query = st.text_input(
                            
                        #         "Ask about report/PDF",

                        #         key=f"report_chat_{idx}"
                        #     )

                        #     if st.button(
                            
                        #         "Ask Report",

                        #         key=f"report_btn_{idx}"
                        #     ):

                        #         vector_db = current_session.get(
                        #             "workflow_result",
                        #             {}
                        #         ).get(
                        #             "vector_db"
                        #         )

                        #         if not vector_db:
                                
                        #             st.error(
                        #                 "No vector database available."
                        #             )

                        #         else:
                                
                        #             with st.spinner(
                        #                 "Searching PDF..."
                        #             ):

                        #                 answer = chat_with_report(
                                        
                        #                     vector_db=vector_db,

                        #                     query=report_query
                        #                 )

                        #             st.write(answer)

                        # =====================================
                        # NORMAL TABS
                        # =====================================

                     
                        
                        tab_data = tab_content[tab_name]

                        if isinstance(
                            tab_data,
                            list
                        ):

                            for item in tab_data:
                            
                                st.markdown(
                                    f"- {item}"
                                )

                        elif isinstance(
                            tab_data,
                            dict
                        ):

                            st.write(
                                tab_data.get(
                                    "content",
                                    ""
                                )
                            )

                            for cite in tab_data.get(
                                "citations",
                                []
                            ):

                                st.markdown(
                                    f"- {cite}"
                                )

                        else:
                        
                            st.write(tab_data)
                    # with tabs[tab_idx]:
                    #     tab_data = tab_content[tab_name]
                    #     if isinstance(tab_data, list):
                    #         for item in tab_data:
                    #             st.markdown(f"- {item}")
                    #     elif isinstance(tab_data, dict):
                    #         st.write(tab_data.get("content", ""))
                    #         for cite in tab_data.get("citations", []):
                    #             st.markdown(f"- {cite}")
                    #     else:
                    #         st.write(tab_data)

            # CHANGE 2: Guard PDF download with valid_report check
            valid_report = (
                isinstance(content, dict)
                and content.get("title")
                and (
                    content.get("abstract")
                    or content.get("dynamic_sections")
                )
            )

            if valid_report:

                pdf_path = generate_pdf_report(content)

                with open(pdf_path, "rb") as f:
                    pdf_bytes = f.read()

                st.download_button(
                    label="⬇️ Download PDF Report",
                    data=pdf_bytes,
                    file_name=f"research_report_{idx}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key=f"download_pdf_{idx}",
                )

        # --------------------------------------------------
        # USER MESSAGE — query + downloadable PDFs
        # --------------------------------------------------
        elif isinstance(content, dict) and "query" in content:
            st.markdown(content.get("query", ""))

            pdfs = content.get("pdfs", [])
            if pdfs:
                st.markdown("**Attached PDFs**")
                for pdf_idx, pdf in enumerate(pdfs):
                    if isinstance(pdf, dict) and "bytes" in pdf:
                        pdf_bytes = base64.b64decode(pdf["bytes"])
                        st.download_button(
                            label=f"📄 {pdf['name']}",
                            data=pdf_bytes,
                            file_name=pdf["name"],
                            mime="application/pdf",
                            key=f"msg_{idx}_pdf_{pdf_idx}",
                        )
                    else:
                        st.markdown(f"📄 {pdf}  *(not available for download)*")

        # --------------------------------------------------
        # PLAIN TEXT
        # --------------------------------------------------
        else:
            st.write(content)

# =========================================================
# WORKFLOW STATE & RESULT
# =========================================================

workflow_running = current_session.get("workflow_running", False)
result = current_session.get("workflow_result")

awaiting_approval = bool(
    result
    and result.get("awaiting_human_approval", False)
    and not result.get("critical_error", False)
)

# =========================================================
# HUMAN APPROVAL
# =========================================================

if awaiting_approval:
    with st.chat_message("assistant"):
        st.subheader("Human Approval Required")

        analysis = result.get("analysis", {})
        validation = result.get("validation", {})

        analysis_tabs = []
        analysis_content = {}

        summary = analysis.get("summary", "")
        if summary:
            analysis_tabs.append("Summary")
            analysis_content["Summary"] = summary

        findings = analysis.get("key_findings", [])
        if findings:
            analysis_tabs.append("Key Findings")
            analysis_content["Key Findings"] = findings

        for section in analysis.get("dynamic_sections", []):
            heading = section.get("heading", "")
            body = section.get("content", "")
            if heading and body:
                analysis_tabs.append(heading)
                analysis_content[heading] = {
                    "content": body,
                    "citations": section.get("citations", []),
                }
       

        if analysis_tabs:
            tabs = st.tabs(analysis_tabs)
            for t_idx, tab_name in enumerate(analysis_tabs):
                with tabs[t_idx]:
                                
                    # =====================================
                    # NORMAL TABS
                    # =====================================
                    
                    tab_data = analysis_content.get(
                            tab_name
                        )
                
                    if isinstance(
                            tab_data,
                            list
                        ):
                
                            for item in tab_data:
                            
                                st.markdown(
                                    f"- {item}"
                                )
                
                    elif isinstance(
                            tab_data,
                            dict
                        ):
                
                            st.write(
                                tab_data.get(
                                    "content",
                                    ""
                                )
                            )
                
                            citations = tab_data.get(
                                "citations",
                                []
                            )
                
                            if citations:
                            
                                st.markdown(
                                    "### Citations"
                                )
                
                                for cite in citations:
                                
                                    st.markdown(
                                        f"- {cite}"
                                    )
                
                    else:
                        
                            st.write(tab_data)
                # with tabs[t_idx]:
                #     tab_data = analysis_content[tab_name]
                #     if isinstance(tab_data, list):
                #         for item in tab_data:
                #             st.markdown(f"- {item}")
                #     elif isinstance(tab_data, dict):
                #         st.write(tab_data.get("content", ""))
                #         for cite in tab_data.get("citations", []):
                #             st.markdown(f"- {cite}")
                #     else:
                #         st.write(tab_data)

        st.markdown("## Validation")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Confidence Score", validation.get("confidence_score", 0.0))
        with col2:
            st.metric(
                "Research Sufficient",
                str(validation.get("research_sufficient", False)),
            )

        validation_summary = validation.get("validation_summary", "")
        if validation_summary:
            st.info(validation_summary)

        user_feedback = st.text_area(
            "Additional Instructions",
            key=f"human_feedback_{st.session_state.current_session_id}",
            placeholder="Add refinement instructions...",
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            approve = st.button("Approve Report")
        with col2:
            refine = st.button("Refine Research")
        with col3:
            stop = st.button("Stop Workflow")

        # APPROVE
        if approve:
            with st.spinner("Generating Final Report..."):
                result["awaiting_human_approval"] = False
                result["next_agent"] = "reporter"

                final_result, hit_error = stream_graph(result, recursion_limit=20)
                SessionManager.save_result(final_result)

                if hit_error:

                    current_session["workflow_running"] = False

                    current_session["workflow_result"] = final_result

                    st.error(
                        "Report generation failed due to API/model error."
                    )

                    st.stop()
                elif (
                    final_result.get("report")
                    and isinstance(final_result["report"], dict)
                    and final_result["report"].get("title")
                ):
                    SessionManager.add_message("assistant", final_result["report"])

                current_session["workflow_running"] = False
                st.session_state["reset_query"] = True
                st.session_state["uploader_reset_counter"] += 1
                st.rerun()

        elif refine:

            with st.spinner("Refining Research..."):


                result["awaiting_human_approval"] = False

                result["human_feedback"] = user_feedback

                result["retries"] = {}

                result["next_agent"] = "human_intent_router"

                # =====================================
                # STORE PREVIOUS SNAPSHOT
                # =====================================

                existing_workflow = current_session.get(
                    "workflow_result",
                    {}
                ) or {}

                # =====================================
                # FALLBACK SAFE LOAD
                # =====================================

                existing_report = (

                    existing_workflow.get(
                        "report",
                        {}
                    )

                    or result.get(
                        "report",
                        {}
                    )
                )

                existing_analysis = (

                    existing_workflow.get(
                        "analysis",
                        {}
                    )

                    or result.get(
                        "analysis",
                        {}
                    )
                )

                # =====================================
                # SAVE PREVIOUS STATE
                # =====================================

                result["previous_report"] = (
                    existing_report
                )

                result["previous_analysis"] = (
                    existing_analysis
                )

                print(
                    "\n========== SAVED PREVIOUS REPORT ==========\n"
                )

                print(
                    result["previous_report"]
                )

                print(
                    "\n========== SAVED PREVIOUS ANALYSIS ==========\n"
                )

                # print(
                #     result["previous_analysis"]
                # )

                # print("\n========== SAVED PREVIOUS REPORT ==========\n")
                # print(result["previous_report"])

                # print("\n========== SAVED PREVIOUS ANALYSIS ==========\n")
                # print(result["previous_analysis"])

                final_result, hit_error = stream_graph(
                    result,
                    recursion_limit=20
                )
                SessionManager.save_result(
                    final_result
                )

                # =====================================
                # ERROR
                # =====================================

                if hit_error:

                    current_session[
                        "workflow_running"
                    ] = False

                    current_session[
                        "workflow_result"
                    ] = final_result


                    st.error(
                        "Research refinement failed."
                    )

                    st.stop()

                # =====================================
                # IMPORTANT FIX
                # =====================================

                if (
    final_result.get("report")
    and isinstance(
        final_result["report"],
        dict
    )
):

                    SessionManager.add_message(

                        "assistant",

                        final_result["report"]
                    )

                # =====================================
                # CLEANUP
                # =====================================

                current_session[
                    "workflow_running"
                ] = False

                current_session[
                    "workflow_result"
                ] = final_result

                st.session_state[
                    "reset_query"
                ] = True

                st.session_state[
                    "uploader_reset_counter"
                ] += 1

                st.rerun()

        # STOP
        elif stop:
            current_session["workflow_result"] = None
            current_session["workflow_running"] = False
            st.session_state["reset_query"] = True
            st.session_state["uploader_reset_counter"] += 1
            st.rerun()

# =========================================================
# INPUT KEY CONSTRUCTION
# =========================================================

query_key = f"query_{st.session_state.current_session_id}"
pdf_uploader_key = (
    f"pdf_uploader_"
    f"{st.session_state.current_session_id}_"
    f"{st.session_state.get('uploader_reset_counter', 0)}"
)

if st.session_state.get("reset_query", False):
    if query_key in st.session_state:
        del st.session_state[query_key]
    st.session_state["reset_query"] = False

if query_key not in st.session_state:
    st.session_state[query_key] = ""

# =========================================================
# QUERY INPUT AREA
# =========================================================

st.divider()

if not workflow_running and not awaiting_approval:

    st.markdown("## New Research Query")

    uploaded_files = st.file_uploader(
        "Upload Research PDFs",
        type=["pdf"],
        accept_multiple_files=True,
        key=pdf_uploader_key,
    )

    query = st.text_area(
        "Enter Research Query",
        key=query_key,
        placeholder="Example: AI in Healthcare and Education",
        height=180,
    )

    generate_btn = st.button("Generate Research Report", use_container_width=True)

else:
    if workflow_running:
        st.info("⏳ Workflow running — please wait...")
    uploaded_files = []
    query = ""
    generate_btn = False

# =========================================================
# GENERATE
# =========================================================

def validate_uploaded_pdf(uploaded_file):

    try:

        if uploaded_file is None:

            return False, (
                "No file provided"
            )

        uploaded_file.seek(0)

        file_bytes = uploaded_file.read()

        uploaded_file.seek(0)

        # =====================================
        # EMPTY FILE
        # =====================================

        if not file_bytes:

            return False, (
                f"{uploaded_file.name} is empty"
            )

        # =====================================
        # CORRUPTED / TOO SMALL
        # =====================================

        if len(file_bytes) < 100:

            return False, (
                f"{uploaded_file.name} appears corrupted"
            )

        # =====================================
        # PDF HEADER CHECK
        # =====================================

        if not file_bytes.startswith(
            b"%PDF"
        ):

            return False, (
                f"{uploaded_file.name} is not a valid PDF"
            )

        return True, ""

    except Exception as e:

        return False, str(e)


if generate_btn:

    if not query.strip():
        st.warning("Please enter a research query.")
        st.stop()

    current_session["workflow_running"] = True

    # =====================================
    # VALIDATE PDFs
    # =====================================

    validation_errors = []

    for uploaded_file in uploaded_files:

        is_valid, error_msg = (

            validate_uploaded_pdf(
                uploaded_file
            )
        )

        if not is_valid:

            validation_errors.append(
                error_msg
            )

    if validation_errors:

        current_session[
            "workflow_running"
        ] = False

        st.error(
            "Invalid PDF file(s) detected"
        )

        for err in validation_errors:

            st.warning(err)

        st.stop()

    pdf_message_entries = []
    uploaded_file_objects = list(uploaded_files)

    for uf in uploaded_file_objects:
        raw = uf.read()
        pdf_message_entries.append({
            "name": uf.name,
            "bytes": base64.b64encode(raw).decode("utf-8"),
        })
        uf.seek(0)

    SessionManager.add_message(
        "user",
        {"query": query, "pdfs": pdf_message_entries},
    )

    progress = st.progress(0)
    status_box = st.empty()
    stream_box = st.empty()
    agent_box = st.empty()
    reasoning_container = st.container()
    try:
        vector_db = None

        if uploaded_file_objects:
            status_box.info("Processing uploaded PDFs…")
            progress.progress(10)

            all_docs = []
            for uf in uploaded_file_objects:
                file_path = save_uploaded_file(uf)
                docs = load_pdf(file_path)

                if not docs:

                    raise ValueError(

                        f"{uf.name} contains "
                        "no readable content"
                    )

                all_docs.extend(docs)

            chunks = split_documents(all_docs)

            if not chunks:

                raise ValueError(

                    "Uploaded PDF contains "
                    "no extractable text"
                )
            # vector_db = create_vectorstore(chunks)
            delete_vectorstore(
    st.session_state.current_session_id
)
            vector_db = create_vectorstore(chunks,st.session_state.current_session_id)
            st.success("PDF processing complete.")
        # =========================================
        # BUILD CONTEXT-AWARE QUERY
        # =========================================
        
        messages = current_session.get(
            "messages",
            []
        )
        
        recent_messages = messages[-6:]
        
        conversation_context = ""
        
        for msg in recent_messages:
        
            role = msg.get(
                "role",
                "user"
            )
        
            content = msg.get(
                "content",
                ""
            )
        
            # =====================================
            # DICTIONARY CONTENT
            # =====================================
        
            if isinstance(content, dict):
        
                content_text = str(content)
        
                # ---------------------------------
                # LARGE REPORTS
                # ---------------------------------
        
                if len(content_text) > 3000:
        
                    try:
        
                        summary_prompt = f"""
        
                        Summarize this research response
                        into concise conversational memory.
        
                        Preserve:
                        - key topics
                        - important findings
                        - conclusions
                        - discussed entities
                        - follow-up relevance
        
                        Keep under 200 words.
        
                        CONTENT:
                        {content_text}
                        """
        
                        summary_response = (
                            reasoning_llm.invoke(
                                summary_prompt
                            )
                        )
        
                        compressed_content = (
                            summary_response.content
                        )
        
                    except Exception:
        
                        compressed_content = (
                            content_text[:1500]
                        )
        
                # ---------------------------------
                # SMALL CONTENT
                # ---------------------------------
        
                else:
        
                    compressed_content = (
                        content_text
                    )
        
                conversation_context += f"""
        
        {role.upper()}:
        {compressed_content}
        
        """
        
            # =====================================
            # NORMAL TEXT MESSAGES
            # =====================================
        
            else:
        
                conversation_context += f"""
        
        {role.upper()}:
        {str(content)}
        
        """

          # =========================================
        # FINAL ENHANCED QUERY
        # =========================================

        enhanced_query = f"""

    Previous Conversation Context:

    {conversation_context}

    Current User Query:

    {query}

    """
        initial_state = {
            "thread_id": st.session_state.current_session_id,
            "query": enhanced_query,
            "subqueries": [],
            "retrieved_docs": [],
            "analysis": {
                "summary": "",
                "confidence_score": 0,
                "key_findings": [],
                "dynamic_sections": []
            },
            "validation": {},
            "report": {
            },
            "citations": [],
            "errors": [],
            "retries": {},
            "critical_error": False,
            "error": {},
            
            "workflow_complete": False,
            "next_agent": "supervisor",
            "vector_db": vector_db,
            "routing": {},
            "pdf_uploaded": bool(uploaded_file_objects),
            "awaiting_human_approval": False,
            "human_feedback": "",
            "validator_feedback":"",
            "section_operation":{},
            "previous_report": {},

"previous_analysis": {},
        }

        progress.progress(25)

        # CHANGE 3: Updated stream execution block — graph.stream inside try,
        # break on critical_error instead of st.rerun(), improved exception handling
        final_result = initial_state.copy()

        streamed_text = ""

        hit_error = False

        try:

            events = graph.stream(

                initial_state,

                config={
                    "recursion_limit": 25
                },

                stream_mode="updates"
            )
            for event in events:
                print("\n" + "=" * 100)
                print("RAW GRAPH EVENT")
                print("=" * 100)

                print(event)

                print("=" * 100 + "\n")
            # for mode, event in events:
                
                for node, value in event.items():

                    print("\n" + "=" * 100)
                    print("NODE EVENT")
                    print("=" * 100)

                    print("NODE:")
                    print(node)

                    print("\nVALUE:")
                    print(value)

                    print("\nVALUE TYPE:")
                    print(type(value))

                    print("\nCRITICAL ERROR:")
                    print(
                        value.get(
                            "critical_error"
                        )
                        if isinstance(
                            value,
                            dict
                        )
                        else None
                    )

                    print("\nERROR:")
                    print(
                        value.get(
                            "error"
                        )
                        if isinstance(
                            value,
                            dict
                        )
                        else None
                    )

                    print("=" * 100 + "\n")

                    agent_box.info(
                        f"Running agent: {node}"
                    )
                    with st.expander(

                        f"{node}",
                    
                        expanded=False
                    ):
                    
                        try:
                            st.json(value)
                        except Exception:
                            st.write(str(value))

                    if isinstance(value, dict):

                        # final_result.update(value)
                        old_vector_db = final_result.get("vector_db")

                        if "analysis" in value:

                            old_analysis = final_result.get(
                                "analysis",
                                {}
                            ) or {}

                            new_analysis = value.get(
                                "analysis",
                                {}
                            ) or {}

                            merged_analysis = old_analysis.copy()

                            # =====================================
                            # DO NOT OVERWRITE WITH EMPTY VALUES
                            # =====================================

                            for k, v in new_analysis.items():

                                if v in [
                                    "",
                                    [],
                                    {},
                                    None
                                ]:
                                    continue

                                merged_analysis[k] = v

                            # =====================================
                            # PRESERVE DYNAMIC SECTIONS
                            # =====================================

                            if new_analysis.get(
                                "dynamic_sections"
                            ):

                                merged_analysis[
                                    "dynamic_sections"
                                ] = new_analysis[
                                    "dynamic_sections"
                                ]

                            final_result[
                                "analysis"
                            ] = merged_analysis
                        if "report" in value:

                            old_report = final_result.get(
                                "report",
                                {}
                            ) or {}

                            new_report = value.get(
                                "report",
                                {}
                            ) or {}

                            # =====================================
                            # IGNORE EMPTY REPORTS
                            # =====================================

                            if not new_report:

                                new_report = {}

                            merged_report = old_report.copy()
                            if not merged_report:

                                merged_report = final_result.get(
                                    "previous_report",
                                    {}
                                ).copy()

                            for k, v in new_report.items():

                                # =====================================
                                # SKIP EMPTY VALUES
                                # =====================================

                                if v in [
                                    "",
                                    [],
                                    {},
                                    None
                                ]:
                                    continue

                                merged_report[k] = v

                            # =====================================
                            # PRESERVE DYNAMIC SECTIONS
                            # =====================================

                            if new_report.get(
                                "dynamic_sections"
                            ):

                                merged_report[
                                    "dynamic_sections"
                                ] = new_report[
                                    "dynamic_sections"
                                ]

                            final_result[
                                "report"
                            ] = merged_report
                        for k, v in value.items():

                            if k not in [
                                "analysis",
                                "report"
                            ]:

                                final_result[k] = v

                        print("\n" + "=" * 100)
                        print("FINAL RESULT AFTER MERGE")
                        print("=" * 100)

                        print("CRITICAL ERROR:")
                        print(
                            final_result.get(
                                "critical_error"
                            )
                        )

                        print("\nERROR:")
                        print(
                            final_result.get(
                                "error"
                            )
                        )

                        print("=" * 100 + "\n")

                        if value.get("error"):

                            final_result["error"] = value["error"]

                            print("\n" + "=" * 100)
                            print("ERROR MERGED INTO FINAL RESULT")
                            print("=" * 100)

                            print("SOURCE ERROR:")
                            print(value["error"])

                            print("\nFINAL RESULT ERROR:")
                            print(final_result.get("error"))

                            print("=" * 100 + "\n")
                    
                        if (
                            final_result.get("vector_db") is None
                            and old_vector_db is not None
                        ):
                            final_result["vector_db"] = old_vector_db
                        status = value.get(
                            "status",
                            ""
                        )

                        if status:

                            status_box.markdown(
                                f"### {status}"
                            )

                        chunk = value.get(
                            "stream_chunk",
                            ""
                        )

                        if chunk:

                            streamed_text += chunk

                            stream_box.markdown(
                                streamed_text + "▌"
                            )
                        
                        # st.error("Frontend received critical_error")
                        # =====================================
                        # CRITICAL ERROR
                        # =====================================

                        if (
                            value.get(
                                "critical_error",
                                False
                            )
                            or
                            final_result.get(
                                "critical_error",
                                False
                            )
                        ):

                            print("\n" + "=" * 100)
                            print("CRITICAL ERROR RECEIVED FROM GRAPH")
                            print("=" * 100)

                            print("NODE:")
                            print(node)

                            print("\nVALUE:")
                            print(value)

                            print("\nFINAL RESULT:")
                            print(final_result)

                            print("=" * 100 + "\n")

                            hit_error = True

                            break

                            raw_errors = final_result.get(
                                "errors",
                                ["Unknown workflow failure"]
                            )

                            current_session[
    "workflow_result"
] = {

    "critical_error":
        True,

    "workflow_complete":
        True,

    "workflow_running":
        False,

    "awaiting_human_approval":
        False,

    "error":
        final_result.get(
            "error",
            {}
        )
}

                            current_session[
                                "workflow_running"
                            ] = False
                            st.error("Saving frontend error message")
   
                            err_title, err_body = classify_error(

    final_result.get(
        "error",
        {}
    )
)

                            st.error(err_title)

                            st.markdown(err_body)
                            progress.empty()

                            status_box.empty()

                            stream_box.empty()

                            agent_box.empty()

                            st.session_state[
                                "reset_query"
                            ] = True

                            st.session_state[
                                "uploader_reset_counter"
                            ] += 1

                            for _ in events:
                                pass
                            
                            break

                if hit_error:
                    break
            
            
            print("\n" + "=" * 100)
            print("STREAM FINISHED")
            print("=" * 100)

            print("HIT ERROR:")
            print(hit_error)

            print("\nFINAL RESULT:")
            print(final_result)

            print("=" * 100 + "\n")

        except Exception as stream_error:
                
            combined = str(
                stream_error
            ).lower()
        
            # =====================================
            # IGNORE NON-FATAL INTERRUPTS
            # =====================================
        
            if "interrupt" in combined:
            
                pass
            
            else:
            
                traceback.print_exc()
        
                hit_error = True
        
                final_result.update({
                
                    "critical_error":
                        True,
        
                    "workflow_complete":
                        True,
        
                    "workflow_running":
                        False,
        
                    "awaiting_human_approval":
                        False,
        
                    "error": {
                    
                        "type":
                            type(stream_error).__name__,
        
                        "message":
                            str(stream_error),
        
                        "raw":
                            traceback.format_exc()
                    },
        
                    "next_agent":
                        "__end__"
                })
        current_session["workflow_result"] = final_result
        progress.progress(100)
        SessionManager.save_result(final_result)

        # CHANGE 4: Updated hit_error block — renders error inline, uses st.stop()
        if hit_error:
        
            print("\n" + "=" * 100)
            print("ENTERED HIT_ERROR BLOCK")
            print("=" * 100)

            print("FINAL RESULT ERROR:")
            print(
                final_result.get(
                    "error",
                    {}
                )
            )

            print("\nFINAL RESULT:")
            print(final_result)

            print("=" * 100 + "\n")

            current_session[
                "workflow_running"
            ] = False

            current_session[
                "workflow_result"
            ] = final_result

            save_error_message(

            final_result.get(
        "error",
        {}
    )
)

            print("\n" + "=" * 100)
            print("AFTER SAVE_ERROR_MESSAGE")
            print("=" * 100)

            msgs = (
                SessionManager
                .get_current_session()
                .get(
                    "messages",
                    []
                )
            )

            print(
                f"MESSAGE COUNT: {len(msgs)}"
            )

            for i, m in enumerate(msgs):
                print(f"\nMESSAGE {i}")
                print(m)

            print("=" * 100 + "\n")

            current_session[
                "workflow_running"
            ] = False

            current_session[
                "workflow_result"
            ] = final_result

            print(
                "\n========== ERROR SAVED =========="
            )

            messages = (
                SessionManager
                .get_current_session()
                .get(
                    "messages",
                    []
                )
            )

            print(
                f"MESSAGE COUNT: {len(messages)}"
            )

            if messages:
                print(
                    "\nLAST MESSAGE:"
                )
                print(
                    messages[-1]
                )

            print(
                "\n================================="
            )

            st.session_state[
                "reset_query"
            ] = True

            st.session_state[
                "uploader_reset_counter"
            ] += 1
            st.rerun()

        elif (
                
            not hit_error
        
            and final_result.get("report")
        
            and isinstance(
                final_result["report"],
                dict
            )
        
            and final_result["report"].get("title")
        
            and (
                final_result["report"].get("abstract")
                or final_result["report"].get("dynamic_sections")
            )
        ):
            SessionManager.add_message("assistant", final_result["report"])

        current_session["workflow_running"] = False

        # =====================================
        # ONLY RESET IF SUCCESS
        # =====================================
        
        if not hit_error:
        
            st.session_state["reset_query"] = True
        
            st.session_state[
                "uploader_reset_counter"
            ] += 1
        
            st.rerun()
    # CHANGE 5: Updated outer exception block — persists result, uses st.rerun()
    except Exception as e:

        raw_tb = traceback.format_exc()

        current_session[
    "workflow_result"
] = {

    "critical_error":
        True,

    "workflow_complete":
        True,

    "workflow_running":
        False,

    "awaiting_human_approval":
        False,

    "error": {

        "type":
            type(e).__name__,

        "message":
            str(e),

        "raw":
            raw_tb
    }
}
        save_error_message(

    current_session[
        "workflow_result"
    ].get(
        "error",
        {}
    )
)
        current_session[
            "workflow_running"
        ] = False

        st.session_state[
            "reset_query"
        ] = True

        st.session_state[
            "uploader_reset_counter"
        ] += 1

        st.rerun()
