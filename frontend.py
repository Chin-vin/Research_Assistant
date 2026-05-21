import os

os.environ["STREAMLIT_WATCHER_TYPE"] = "none"

import time
import base64

import streamlit as st

from session_manager import (
    SessionManager
)

from workflow.graph import graph

from utils.pdf_generator import (
    generate_pdf_report
)

from utils.file_handler import (
    save_uploaded_file
)

from rag.loader import load_pdf

from rag.splitter import (
    split_documents
)

from rag.vectorstore import (
    create_vectorstore
)

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(

    page_title="Intelligent Research Assistant",

    page_icon="📘",

    layout="wide"
)
if "uploader_reset_counter" not in st.session_state:

    st.session_state[
        "uploader_reset_counter"
    ] = 0
# =========================================================
# SESSION INITIALIZATION
# =========================================================

SessionManager.initialize()

current_session = (
    SessionManager.get_current_session()
)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title(
        "Research Assistant"
    )

    st.divider()

    st.subheader(
        "Research Sessions"
    )

    # -----------------------------------------------------
    # NEW SESSION
    # -----------------------------------------------------

    if st.button(
        "New Session",
        use_container_width=True
    ):

        SessionManager.create_new_session()

        st.rerun()

    st.divider()

    # -----------------------------------------------------
    # SESSION LIST
    # -----------------------------------------------------

    sessions = st.session_state.sessions

    sorted_sessions = list(
        sessions.keys()
    )[::-1]

    for session_id in sorted_sessions:

        button_type = (
            "primary"
            if session_id
            == st.session_state.current_session_id
            else "secondary"
        )

        if st.button(

            session_id[:8],

            key=session_id,

            use_container_width=True,

            type=button_type
        ):

            st.session_state.current_session_id = (
                session_id
            )

            st.rerun()

# =========================================================
# REFRESH SESSION
# =========================================================

current_session = (
    SessionManager.get_current_session()
)

# =========================================================
# HEADER
# =========================================================

st.title(
    "Intelligent Research Assistant"
)

# =========================================================
# CHAT HISTORY
# =========================================================
messages = current_session.get(
    "messages",
    []
)

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

# =========================================================
# RENDER CHAT HISTORY
# =========================================================

for idx, msg in enumerate(messages):

    with st.chat_message(
        msg["role"]
    ):

        content = msg["content"]

        # =================================================
        # REPORT MESSAGE
        # =================================================

        if isinstance(content, dict):

            title = content.get(
                "title",
                "Research Report"
            )

            st.subheader(title)

            # =================================================
            # DYNAMIC TAB CREATION
            # =================================================

            available_tabs = []

            tab_content = {}

            # -------------------------------------------------
            # ABSTRACT
            # -------------------------------------------------

            abstract = content.get(
                "abstract",
                ""
            )

            if abstract:

                available_tabs.append(
                    "Abstract"
                )

                tab_content[
                    "Abstract"
                ] = abstract

            # -------------------------------------------------
            # INTRODUCTION
            # -------------------------------------------------

            introduction = content.get(
                "introduction",
                ""
            )

            if introduction:

                available_tabs.append(
                    "Introduction"
                )

                tab_content[
                    "Introduction"
                ] = introduction

            # -------------------------------------------------
            # METHODOLOGY
            # -------------------------------------------------

            methodology = content.get(
                "methodology",
                ""
            )

            if methodology:

                available_tabs.append(
                    "Methodology"
                )

                tab_content[
                    "Methodology"
                ] = methodology

            # -------------------------------------------------
            # KEY FINDINGS
            # -------------------------------------------------

            findings = content.get(
                "key_findings",
                []
            )

            if findings:

                available_tabs.append(
                    "Key Findings"
                )

                tab_content[
                    "Key Findings"
                ] = findings

            # -------------------------------------------------
            # DYNAMIC SECTIONS
            # -------------------------------------------------

            dynamic_sections = content.get(
                "dynamic_sections",
                []
            )

            for section in dynamic_sections:

                heading = section.get(
                    "heading",
                    ""
                )

                body = section.get(
                    "content",
                    ""
                )

                citations = section.get(
                    "citations",
                    []
                )

                if heading and body:

                    available_tabs.append(
                        heading
                    )

                    tab_content[
                        heading
                    ] = {

                        "content": body,

                        "citations": citations
                    }

            # -------------------------------------------------
            # CONCLUSION
            # -------------------------------------------------

            conclusion = content.get(
                "conclusion",
                ""
            )

            if conclusion:

                available_tabs.append(
                    "Conclusion"
                )

                tab_content[
                    "Conclusion"
                ] = conclusion

            # -------------------------------------------------
            # REFERENCES
            # -------------------------------------------------

            references = content.get(
                "references",
                []
            )

            if references:

                available_tabs.append(
                    "References"
                )

                tab_content[
                    "References"
                ] = references

            # =================================================
            # CREATE TABS
            # =================================================

            if available_tabs:

                tabs = st.tabs(
                    available_tabs
                )

                for tab_idx, tab_name in enumerate(
                    available_tabs
                ):

                    with tabs[tab_idx]:

                        tab_data = tab_content[
                            tab_name
                        ]

                        # ----------------------------
                        # LIST CONTENT
                        # ----------------------------

                        if isinstance(
                            tab_data,
                            list
                        ):

                            for item in tab_data:

                                st.markdown(
                                    f"- {item}"
                                )

                        # ----------------------------
                        # DICT CONTENT
                        # ----------------------------

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

                        # ----------------------------
                        # STRING CONTENT
                        # ----------------------------

                        else:

                            st.write(tab_data)

            # =================================================
            # PDF DOWNLOAD
            # =================================================

            pdf_path = generate_pdf_report(
                content
            )

            with open(
                pdf_path,
                "rb"
            ) as pdf_file:

                pdf_bytes = pdf_file.read()

            st.download_button(

                label="Download PDF Report",

                data=pdf_bytes,

                file_name=(
                    f"research_report_{idx}.pdf"
                ),

                mime="application/pdf",

                use_container_width=True,

                key=f"download_pdf_{idx}"
            )

        # =================================================
        # NORMAL MESSAGE
        # =================================================

        else:

            st.write(content)
# =========================================================
# WORKFLOW STATE
# =========================================================

workflow_running = current_session.get(
    "workflow_running",
    False
)

# =========================================================
# GENERATE WORKFLOW
# =========================================================

if workflow_running:

    progress = st.progress(0)

    status_box = st.empty()

    stream_box = st.empty()

    agent_box = st.empty()

# =========================================================
# WORKFLOW RESULT
# =========================================================

result = current_session.get(
    "workflow_result"
)

# =========================================================
# HUMAN APPROVAL
# =========================================================

if (

    result

    and result.get(
        "awaiting_human_approval",
        False
    )
):

    with st.chat_message("assistant"):

        st.subheader(
            "Human Approval Required"
        )

        analysis = result.get(
            "analysis",
            {}
        )

        validation = result.get(
            "validation",
            {}
        )

        # =====================================================
        # DYNAMIC ANALYSIS TABS
        # =====================================================

        analysis_tabs = []

        analysis_content = {}

        # -----------------------------------------------------
        # SUMMARY
        # -----------------------------------------------------

        summary = analysis.get(
            "summary",
            ""
        )

        if summary:
        
            analysis_tabs.append(
                "Summary"
            )

            analysis_content[
                "Summary"
            ] = summary

        # -----------------------------------------------------
        # KEY FINDINGS
        # -----------------------------------------------------

        findings = analysis.get(
            "key_findings",
            []
        )

        if findings:
        
            analysis_tabs.append(
                "Key Findings"
            )

            analysis_content[
                "Key Findings"
            ] = findings

        # -----------------------------------------------------
        # DYNAMIC SECTIONS
        # -----------------------------------------------------

        dynamic_sections = analysis.get(
            "dynamic_sections",
            []
        )

        for section in dynamic_sections:
        
            heading = section.get(
                "heading",
                ""
            )

            content = section.get(
                "content",
                ""
            )

            citations = section.get(
                "citations",
                []
            )

            if heading and content:
            
                analysis_tabs.append(
                    heading
                )

                analysis_content[
                    heading
                ] = {
                
                    "content": content,

                    "citations": citations
                }

        # -----------------------------------------------------
        # CREATE TABS
        # -----------------------------------------------------

        if analysis_tabs:
        
            tabs = st.tabs(
                analysis_tabs
            )

            for idx, tab_name in enumerate(
                analysis_tabs
            ):

                with tabs[idx]:
                
                    tab_data = analysis_content[
                        tab_name
                    ]

                    # -----------------------------------------
                    # LIST
                    # -----------------------------------------

                    if isinstance(
                        tab_data,
                        list
                    ):

                        for item in tab_data:
                        
                            st.markdown(
                                f"- {item}"
                            )

                    # -----------------------------------------
                    # DICT
                    # -----------------------------------------

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

                    # -----------------------------------------
                    # STRING
                    # -----------------------------------------

                    else:
                    
                        st.write(tab_data)

        # =====================================================
        # VALIDATION
        # =====================================================

        st.markdown(
            "## Validation"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(

                "Confidence Score",

                validation.get(
                    "confidence_score",
                    0.0
                )
            )

        with col2:

            st.metric(

                "Research Sufficient",

                str(
                    validation.get(
                        "research_sufficient",
                        False
                    )
                )
            )

        validation_summary = validation.get(
            "validation_summary",
            ""
        )

        if validation_summary:

            st.info(
                validation_summary
            )

        # =====================================================
        # FEEDBACK
        # =====================================================

        user_feedback = st.text_area(

            "Additional Instructions",

            key=f"human_feedback_{st.session_state.current_session_id}",

            placeholder=(
                "Add refinement instructions..."
            )
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            approve = st.button(
                "Approve Report"
            )

        with col2:

            refine = st.button(
                "Refine Research"
            )

        with col3:

            stop = st.button(
                "Stop Workflow"
            )

        # =====================================================
        # APPROVE
        # =====================================================

        if approve:

            with st.spinner(
                "Generating Final Report..."
            ):

                result[
                    "awaiting_human_approval"
                ] = False

                result[
                    "next_agent"
                ] = "reporter"

                events = graph.stream(

                    result,

                    config={
                        "recursion_limit": 20
                    },

                    stream_mode="updates"
                )

                final_result = result.copy()

                for event in events:

                    for node, value in event.items():

                        if isinstance(value, dict):

                            final_result.update(
                                value
                            )

                SessionManager.save_result(
                    final_result
                )

                if final_result.get("report"):

                    SessionManager.add_message(

                        "assistant",

                        final_result["report"]
                    )

                current_session[
                    "workflow_running"
                ] = False

                st.rerun()

        # =====================================================
        # REFINE
        # =====================================================

        elif refine:

            with st.spinner(
                "Refining Research..."
            ):

                result[
                    "awaiting_human_approval"
                ] = False

                result[
                    "human_feedback"
                ] = user_feedback

                result[
                    "next_agent"
                ] = "human_intent_router"

                events = graph.stream(

                    result,

                    config={
                        "recursion_limit": 20
                    },

                    stream_mode="updates"
                )

                final_result = result.copy()

                for event in events:

                    for node, value in event.items():

                        if isinstance(value, dict):

                            final_result.update(
                                value
                            )

                SessionManager.save_result(
                    final_result
                )

                st.rerun()

        # =====================================================
        # STOP
        # =====================================================

        elif stop:

            current_session[
                "workflow_result"
            ] = None

            st.warning(
                "Workflow stopped."
            )

            st.stop()
# =========================================================
# RESET QUERY STATE
# =========================================================

query_key = (
    f"query_{st.session_state.current_session_id}"
)

pdf_uploader_key = (
    f"pdf_uploader_"
    f"{st.session_state.current_session_id}_"
    f"{st.session_state.get('uploader_reset_counter', 0)}"
)
# ---------------------------------------------------------
# RESET INPUTS AFTER WORKFLOW
# ---------------------------------------------------------

if st.session_state.get(
    "reset_query",
    False
):

    if query_key in st.session_state:

        del st.session_state[query_key]


    st.session_state[
        "reset_query"
    ] = False
# =========================================================
# QUERY INPUT AREA
# =========================================================

st.divider()

query_key = (
    f"query_"
    f"{st.session_state.current_session_id}"
)

pdf_key = (
    f"pdf_"
    f"{st.session_state.current_session_id}"
)

if query_key not in st.session_state:

    st.session_state[
        query_key
    ] = ""


if not workflow_running:

    st.markdown(
        "## New Research Query"
    )

    uploaded_files = st.file_uploader(

        "Upload Research PDFs",

        type=["pdf"],

        accept_multiple_files=True,

        key=pdf_uploader_key
    )

    query = st.text_area(

        "Enter Research Query",

        key=query_key,

        placeholder=(
            "Example: AI in Healthcare "
            "and Education"
        ),

        height=180
    )

    generate_btn = st.button(

        "Generate Research Report",

        use_container_width=True
    )

else:

    st.info(
        "Workflow Running..."
    )

    uploaded_files = []

    query = ""

    generate_btn = False

# =========================================================
# GENERATE BUTTON
# =========================================================

if generate_btn:

    if not query.strip():

        st.warning(
            "Please enter a research query."
        )

        st.stop()

    # -----------------------------------------------------
    # WORKFLOW FLAG
    # -----------------------------------------------------

    current_session[
        "workflow_running"
    ] = True

    # -----------------------------------------------------
    # SAVE USER MESSAGE
    # -----------------------------------------------------

    SessionManager.add_message(
        "user",
        query
    )
    
    progress = st.progress(0)

    status_box = st.empty()

    stream_box = st.empty()

    agent_box = st.empty()

    try:

        # =================================================
        # PDF PROCESSING
        # =================================================

        vector_db = None

        if uploaded_files:

            status_box.info(
                "Processing Uploaded PDFs..."
            )

            progress.progress(10)

            all_docs = []

            for uploaded_file in uploaded_files:

                file_path = save_uploaded_file(
                    uploaded_file
                )

                docs = load_pdf(
                    file_path
                )

                all_docs.extend(
                    docs
                )

            chunks = split_documents(
                all_docs
            )

            vector_db = create_vectorstore(
                chunks
            )

            st.success(
                "PDF Processing Complete"
            )

        # =================================================
        # INITIAL STATE
        # =================================================

        initial_state = {

            "thread_id":
                st.session_state.current_session_id,

            "query":
                query,

            "subqueries":
                [],

            "retrieved_docs":
                [],

            "analysis":
                {},

            "validation":
                {},

            "report":
                {},

            "citations":
                [],

            "errors":
                [],

            "workflow_complete":
                False,

            "next_agent":
                "supervisor",

            "vector_db":
                vector_db,

            "routing":
                {},

            "pdf_uploaded":
                bool(uploaded_files),

            "awaiting_human_approval":
                False,

            "human_feedback":
                ""
        }

        progress.progress(25)

        events = graph.stream(

            initial_state,

            config={
                "recursion_limit": 25
            },

            stream_mode="updates"
        )

        final_result = initial_state.copy()

        streamed_text = ""

        for event in events:

            for node, value in event.items():

                agent_box.info(
                    f"Running Agent: {node}"
                )

                if isinstance(value, dict):

                    final_result.update(
                        value
                    )

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

        result = final_result

        progress.progress(100)

        SessionManager.save_result(
            result
        )

        if result.get("report"):

            SessionManager.add_message(

                "assistant",

                result["report"]
            )

        current_session[
            "workflow_running"
        ] = False
                # -----------------------------------------------------
        # RESET QUERY INPUTS
        # -----------------------------------------------------

        st.session_state[
            "reset_query"
        ] = True
        st.session_state[
    "uploader_reset_counter"
] += 1
        st.rerun()

    except Exception as e:

        current_session[
            "workflow_running"
        ] = False
        # -----------------------------------------------------
        # RESET QUERY INPUTS
        # -----------------------------------------------------
        
        st.session_state[
            "reset_query"
        ] = True
        st.session_state[
    "uploader_reset_counter"
] += 1
        st.error(
            f"Workflow Failed: {str(e)}"
        )

        st.exception(e)

# =========================================================
# SYSTEM LOGS
# =========================================================

if result and result.get("errors"):

    with st.expander(
        "System Logs / Errors"
    ):

        st.write(
            result["errors"]
        )
