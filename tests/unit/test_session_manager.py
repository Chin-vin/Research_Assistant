# =========================================================
# tests/unit/test_session_manager.py
# =========================================================

from session_manager import (
    SessionManager
)

import streamlit as st


def test_session_init():

    SessionManager.initialize()

    assert (
        "sessions"
        in st.session_state
    )