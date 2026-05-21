import streamlit as st

import uuid


class SessionManager:

    @staticmethod
    def initialize():

        if "sessions" not in st.session_state:

            st.session_state.sessions = {}

        if "current_session_id" not in st.session_state:

            session_id = str(
                uuid.uuid4()
            )

            st.session_state.current_session_id = (
                session_id
            )

            st.session_state.sessions[
                session_id
            ] = {

                "messages": [],

                "workflow_state": {},

                "report": None,

                "awaiting_human_approval": False
            }

    @staticmethod
    def create_new_session():

        session_id = str(
            uuid.uuid4()
        )

        st.session_state.sessions[
            session_id
        ] = {

            "messages": [],

            "workflow_state": {},

            "report": None,

            "awaiting_human_approval": False
        }

        st.session_state.current_session_id = (
            session_id
        )

    @staticmethod
    def get_current_session():

        session_id = st.session_state[
            "current_session_id"
        ]

        return st.session_state.sessions[
            session_id
        ]

    @staticmethod
    def update_current_session(
        key,
        value
    ):

        session_id = st.session_state[
            "current_session_id"
        ]

        st.session_state.sessions[
            session_id
        ][key] = value
    
    @staticmethod
    def add_message(role, content):

        current = (
            SessionManager.get_current_session()
        )

        current["messages"].append({

            "role": role,

            "content": content
        })
    
    @staticmethod
    def save_result(result):

        current = (
            SessionManager.get_current_session()
        )

        current["workflow_result"] = result
