import streamlit as st
import uuid



class SessionManager:

    @staticmethod
    def initialize():

        # Run once per app start
        # if "chroma_initialized" not in st.session_state:

        #     cleanup_all_vectorstores()

        #     st.session_state[
        #         "chroma_initialized"
        #     ] = True

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

                "workflow_result": None,

                "report": None,

                "awaiting_human_approval": False,

                "workflow_running": False
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

            "workflow_result": None,

            "report": None,

            "awaiting_human_approval": False,

            "workflow_running": False
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
    def add_message(
        role,
        content
    ):

        print("\n========== ADD_MESSAGE EXECUTED ==========")

        print("ROLE:")
        print(role)

        print("\nCONTENT:")
        print(content)

        current = (
            SessionManager.get_current_session()
        )

        print("\nBEFORE APPEND:")
        print(current.get("messages", []))

        current["messages"].append({

            "role": role,

            "content": content
        })

        print("\nAFTER APPEND:")
        print(current["messages"])

        print(
            f"\nMESSAGE COUNT: {len(current['messages'])}"
        )

        print("=" * 100 + "\n")

    @staticmethod
    def save_result(result):

        current = (
            SessionManager.get_current_session()
        )

        current["workflow_result"] = result
# # import streamlit as st

# # import uuid
# # from rag.vectorstore import (
# #     cleanup_all_vectorstores,
# #     delete_vectorstore
# # )


# # class SessionManager:

# #     @staticmethod
# #     def initialize():

# #         if "sessions" not in st.session_state:

# #             st.session_state.sessions = {}

# #         if "current_session_id" not in st.session_state:

# #             session_id = str(
# #                 uuid.uuid4()
# #             )

# #             st.session_state.current_session_id = (
# #                 session_id
# #             )

# #             st.session_state.sessions[
# #                 session_id
# #             ] = {

# #                 "messages": [],

# #                 "workflow_state": {},

# #                 "report": None,

# #                 "awaiting_human_approval": False
# #             }

# #     @staticmethod
# #     def create_new_session():

# #         session_id = str(
# #             uuid.uuid4()
# #         )

# #         st.session_state.sessions[
# #             session_id
# #         ] = {

# #             "messages": [],

# #             "workflow_state": {},

# #             "report": None,

# #             "awaiting_human_approval": False
# #         }

# #         st.session_state.current_session_id = (
# #             session_id
# #         )

# #     @staticmethod
# #     def get_current_session():

# #         session_id = st.session_state[
# #             "current_session_id"
# #         ]

# #         return st.session_state.sessions[
# #             session_id
# #         ]

# #     @staticmethod
# #     def update_current_session(
# #         key,
# #         value
# #     ):

# #         session_id = st.session_state[
# #             "current_session_id"
# #         ]

# #         st.session_state.sessions[
# #             session_id
# #         ][key] = value
    
# #     @staticmethod
# #     def add_message(role, content):

# #         current = (
# #             SessionManager.get_current_session()
# #         )

# #         current["messages"].append({

# #             "role": role,

# #             "content": content
# #         })
    
# #     @staticmethod
# #     def save_result(result):

# #         current = (
# #             SessionManager.get_current_session()
# #         )

# #         current["workflow_result"] = result
# import streamlit as st
# import uuid

# from rag.vectorstore import (
#     cleanup_all_vectorstores
# )


# class SessionManager:

#     @staticmethod
#     def initialize():

#         # Run once per application startup
#         if "chroma_initialized" not in st.session_state:

#             cleanup_all_vectorstores()

#             st.session_state[
#                 "chroma_initialized"
#             ] = True

#         if "sessions" not in st.session_state:

#             st.session_state.sessions = {}

#         if "current_session_id" not in st.session_state:

#             session_id = str(
#                 uuid.uuid4()
#             )

#             st.session_state.current_session_id = (
#                 session_id
#             )

#             st.session_state.sessions[
#                 session_id
#             ] = {

#                 "messages": [],

#                 "workflow_state": {},

#                 "workflow_result": None,

#                 "report": None,

#                 "awaiting_human_approval": False,

#                 "workflow_running": False
#             }

#     @staticmethod
#     def create_new_session():

#         session_id = str(
#             uuid.uuid4()
#         )

#         st.session_state.sessions[
#             session_id
#         ] = {

#             "messages": [],

#             "workflow_state": {},

#             "workflow_result": None,

#             "report": None,

#             "awaiting_human_approval": False,

#             "workflow_running": False
#         }

#         st.session_state.current_session_id = (
#             session_id
#         )

#     @staticmethod
#     def get_current_session():

#         session_id = st.session_state[
#             "current_session_id"
#         ]

#         return st.session_state.sessions[
#             session_id
#         ]

#     @staticmethod
#     def update_current_session(
#         key,
#         value
#     ):

#         session_id = st.session_state[
#             "current_session_id"
#         ]

#         st.session_state.sessions[
#             session_id
#         ][key] = value

#     @staticmethod
#     def add_message(
#         role,
#         content
#     ):

#         current = (
#             SessionManager.get_current_session()
#         )

#         current["messages"].append({

#             "role": role,

#             "content": content
#         })

#     @staticmethod
#     def save_result(result):

#         current = (
#             SessionManager.get_current_session()
#         )

#         current["workflow_result"] = result