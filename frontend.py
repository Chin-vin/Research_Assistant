
import os
import base64
import traceback
from dotenv import load_dotenv
from models.llm_registry import reasoning_llm
load_dotenv()
os.environ["STREAMLIT_SERVER_FILE_WATCHER_TYPE"] = "none"

import streamlit as st
import warnings
from rag.vectorstore import (
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

if "uploader_reset_counter" not in st.session_state:
    st.session_state["uploader_reset_counter"] = 0

# =========================================================
# ERROR CLASSIFICATION
# =========================================================

# CHANGE 1: Updated _ERROR_RULES with additional rate-limit patterns
_ERROR_RULES = [
    (
        [
            "rate limit",
            "429",
            "quota",
            "too many requests",
            "resource exhausted",
            "groqerror",
            "rate_limit_exceeded",
            "tokens per day",
            "requested"
        ],
        "Rate limit reached — report could not be generated",
        (
            "The AI model has hit its request limit. "
            "Please wait a minute and try again. "
            "If this keeps happening, try a shorter query or fewer uploaded PDFs."
        ),
    ),
    (
        ["timeout", "timed out", "connection", "network"],
        "Connection issue — report could not be generated",
        (
            "The request timed out while reaching the AI model. "
            "Please check your connection and try again."
        ),
    ),
    (
        ["validationerror", "schema", "json"],
        "Response format error — report could not be generated",
        (
            "The AI model returned an unexpected response format. "
            "This is usually temporary — please try again. "
            "If it repeats, try rephrasing your query."
        ),
    ),
    (
        ["recursion"],
        "Workflow depth exceeded — report could not be generated",
        (
            "The research workflow ran too many steps without finishing. "
            "Try a more focused query or reduce the scope of your research."
        ),
    ),
    (
        ["context length", "token", "maximum context", "prompt too long"],
        "Input too large — report could not be generated",
        (
            "Your query or uploaded documents exceed the model's input limit. "
            "Try uploading fewer or smaller PDFs, or shorten your query."
        ),
    ),
]

_FALLBACK_TITLE = "Unexpected error — report could not be generated"
_FALLBACK_BODY = (
    "Something went wrong while generating your research report. "
    "Please try again. If the problem continues, start a new session."
)


def classify_error(raw_errors: list) -> tuple:
    combined = " ".join(str(e) for e in raw_errors).lower()
    for patterns, title, body in _ERROR_RULES:
        if any(p in combined for p in patterns):
            return title, body
    return _FALLBACK_TITLE, _FALLBACK_BODY


def save_error_message(raw_errors: list):
    """Classify and persist an error as an assistant chat message."""
    err_title, err_body = classify_error(raw_errors)
    SessionManager.add_message(
        "assistant",
        {
            "_type": "workflow_error",   # checked FIRST in render loop
            "title": err_title,
            "message": err_body,
            "errors": raw_errors,
        },
    )


def stream_graph(state, recursion_limit=20):
    """
    Run graph.stream, collect merged result.
    Returns (final_result, hit_critical_error: bool).
    """
    events = graph.stream(
        state,
        config={"recursion_limit": recursion_limit},
        stream_mode="updates",
    )
    merged = state.copy()
    for event in events:
        for node, value in event.items():
            if isinstance(value, dict):
                merged.update(value)
                if value.get("critical_error"):
                    for _ in events:   # drain so graph cleans up
                        pass
                    return merged, True
    return merged, False


# =========================================================
# SESSION INITIALIZATION
# =========================================================

SessionManager.initialize()
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

st.title("Intelligent Research Assistant")

# =========================================================
# CHAT HISTORY
# =========================================================

messages = current_session.get("messages", [])

if not messages:
    st.markdown(
        """
        ### Generate professional research reports

        Features:
        - Multi-Agent RAG
        - Human Approval
        - PDF Upload
        - Dynamic Research Sections
        - Vector Search
        - Streaming Responses
        """
    )

for idx, msg in enumerate(messages):
    with st.chat_message(msg["role"]):
        content = msg["content"]

        # --------------------------------------------------
        # CHECK _type FIRST — before any other dict check
        # This must be first because workflow_error dicts
        # also contain a "title" key which would otherwise
        # match the report condition below.
        # --------------------------------------------------
        if isinstance(content, dict) and content.get("_type") == "workflow_error":
            st.error(f"**{content.get('title', 'Workflow Failed')}**")
            st.markdown(content.get("message", ""))
            st.info("You can start a new query below.")
            errors = content.get("errors", [])
            if errors:
                with st.expander("Technical details"):
                    for err in errors:
                        st.code(str(err))

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
            if references:
                available_tabs.append("References")
                tab_content["References"] = references

            if available_tabs:
                tabs = st.tabs(available_tabs)
                for tab_idx, tab_name in enumerate(available_tabs):
                    with tabs[tab_idx]:
                        tab_data = tab_content[tab_name]
                        if isinstance(tab_data, list):
                            for item in tab_data:
                                st.markdown(f"- {item}")
                        elif isinstance(tab_data, dict):
                            st.write(tab_data.get("content", ""))
                            for cite in tab_data.get("citations", []):
                                st.markdown(f"- {cite}")
                        else:
                            st.write(tab_data)

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
                    tab_data = analysis_content[tab_name]
                    if isinstance(tab_data, list):
                        for item in tab_data:
                            st.markdown(f"- {item}")
                    elif isinstance(tab_data, dict):
                        st.write(tab_data.get("content", ""))
                        for cite in tab_data.get("citations", []):
                            st.markdown(f"- {cite}")
                    else:
                        st.write(tab_data)

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

                    save_error_message(
                        final_result.get(
                            "errors",
                            ["Unknown workflow failure"]
                        )
                    )

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

        # REFINE
        elif refine:
            with st.spinner("Refining Research..."):
                result["awaiting_human_approval"] = False
                result["human_feedback"] = user_feedback
                # result["errors"] = []

                # Reset retries for new refinement cycle

                result["retries"] = {}
                result["next_agent"] = "human_intent_router"

                final_result, hit_error = stream_graph(result, recursion_limit=20)
                SessionManager.save_result(final_result)

                if hit_error:

                   current_session["workflow_running"] = False

                   current_session["workflow_result"] = final_result

                   save_error_message(
                       final_result.get(
                           "errors",
                           ["Unknown workflow failure"]
                       )
                   )

                   st.error(
                       "Research refinement failed due to API/model error."
                   )

                   st.stop()

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

if generate_btn:

    if not query.strip():
        st.warning("Please enter a research query.")
        st.stop()

    current_session["workflow_running"] = True

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
                all_docs.extend(docs)

            chunks = split_documents(all_docs)
            # vector_db = create_vectorstore(chunks)
#             delete_vectorstore(
#     st.session_state.current_session_id
# )
            vector_db = create_vectorstore(chunks,st.session_state.current_session_id)
            st.info("vector db created")
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
            "query": query,
            "subqueries": [],
            "retrieved_docs": [],
            "analysis": {},
            "validation": {},
            "report": {},
            "citations": [],
            "errors": [],
            "retries": {},
            "workflow_complete": False,
            "next_agent": "supervisor",
            "vector_db": vector_db,
            "routing": {},
            "pdf_uploaded": bool(uploaded_file_objects),
            "awaiting_human_approval": False,
            "human_feedback": "",
            "validator_feedback":""
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
            # for mode, event in events:
                
                for node, value in event.items():

                    agent_box.info(
                        f"Running agent: {node}"
                    )
                    with st.expander(

                        f"{node}",
                    
                        expanded=False
                    ):
                    
                        st.json(value)

                    if isinstance(value, dict):

                        # final_result.update(value)
                        old_vector_db = final_result.get("vector_db")

                        final_result.update(value)
                    
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

                        if value.get(
                            "critical_error",
                            False
                        ):

                            hit_error = True

                            final_result.update(value)

                            raw_errors = final_result.get(
                                "errors",
                                ["Unknown workflow failure"]
                            )

                            current_session[
                                "workflow_result"
                            ] = {
                                "critical_error": True,
                                "errors": raw_errors
                            }

                            current_session[
                                "workflow_running"
                            ] = False
                            st.error("Saving frontend error message")
                            save_error_message(

                                final_result.get(
                                    "errors",
                                    ["Unknown workflow failure"]
                                )
                            )

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

                            break

                if hit_error:
                    break
            
            

        except Exception as stream_error:

            traceback.print_exc()   
          

            st.error("GRAPH.STREAM FAILED")

            st.code(str(stream_error))

            st.code(traceback.format_exc())

            hit_error = True

            final_result.update({

                "critical_error": True,

                "workflow_complete": True,

                "workflow_running": False,

                "awaiting_human_approval": False,

                "errors": [
                    str(stream_error),
                    traceback.format_exc()
                ]
            })

        progress.progress(100)
        SessionManager.save_result(final_result)

        # CHANGE 4: Updated hit_error block — renders error inline, uses st.stop()
        if hit_error:
        
            current_session[
                "workflow_running"
            ] = False

            current_session[
                "workflow_result"
            ] = final_result

            raw_errors = final_result.get(
                "errors",
                ["Unknown workflow failure"]
            )

            err_title, err_body = classify_error(
                raw_errors
            )

            # =====================================
            # SAVE ERROR INTO CHAT HISTORY
            # =====================================

            

            st.session_state[
                "reset_query"
            ] = True

            st.session_state[
                "uploader_reset_counter"
            ] += 1
            # st.rerun()
            st.stop()

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
    # CHANGE 5: Updated outer exception block — persists result, uses st.stop()
    except Exception as e:

        raw_tb = traceback.format_exc()

        current_session[
            "workflow_result"
        ] = {

            "critical_error": True,

            "workflow_complete": True,

            "errors": [
                str(e),
                raw_tb
            ]
        }

        save_error_message([
            str(e),
            raw_tb
        ])

        current_session[
            "workflow_running"
        ] = False

        st.session_state[
            "reset_query"
        ] = True

        st.session_state[
            "uploader_reset_counter"
        ] += 1

        st.stop()
