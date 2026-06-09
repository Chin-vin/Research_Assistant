import os
import shutil

from langchain_community.vectorstores import Chroma
from core.singletons import get_embeddings

embedding_model = get_embeddings()

BASE_CHROMA_DIR = "./chroma_db"


# =========================================================
# APP STARTUP CLEANUP
# =========================================================
def cleanup_all_vectorstores():

    try:

        if os.path.exists(BASE_CHROMA_DIR):

            print("\n===== STARTUP CLEANUP =====")

            shutil.rmtree(
                BASE_CHROMA_DIR,
                ignore_errors=True
            )

            print(
                "ALL OLD VECTORSTORES REMOVED"
            )

        os.makedirs(
            BASE_CHROMA_DIR,
            exist_ok=True
        )

    except Exception as e:

        print(
            f"STARTUP CLEANUP FAILED: {e}"
        )


# =========================================================
# DELETE SESSION VECTORSTORE
# =========================================================
def delete_vectorstore(thread_id):

    persist_directory = (
        f"{BASE_CHROMA_DIR}/{thread_id}"
    )

    try:

        if os.path.exists(
            persist_directory
        ):

            print(
                f"\nDELETING VECTORSTORE: {thread_id}"
            )

            shutil.rmtree(
                persist_directory,
                ignore_errors=True
            )

    except Exception as e:

        print(
            f"DELETE FAILED: {e}"
        )

def create_vectorstore(
    chunks,
    thread_id
):

    if not chunks:

        raise ValueError(
            "No chunks available."
        )

    persist_directory = (
        f"{BASE_CHROMA_DIR}/{thread_id}"
    )

    collection_name = (
        f"collection_{thread_id}"
    )

    os.makedirs(
        persist_directory,
        exist_ok=True
    )

    print(
        f"\nCREATING VECTORSTORE FOR {thread_id}"
    )

    db = Chroma.from_documents(

        documents=chunks,

        embedding=embedding_model,

        persist_directory=persist_directory,

        collection_name=collection_name
    )

    db.persist()

    print(
        "\nVECTORSTORE CREATED"
    )

    return db
# =========================================================
# CREATE VECTORSTORE
# # =========================================================
# def create_vectorstore(
#     chunks,
#     thread_id
# ):

#     if not chunks:

#         raise ValueError(
#             "No chunks available."
#         )

#     delete_vectorstore(
#         thread_id
#     )

#     persist_directory = (
#         f"{BASE_CHROMA_DIR}/{thread_id}"
#     )

#     collection_name = (
#         f"collection_{thread_id}"
#     )

#     os.makedirs(
#         persist_directory,
#         exist_ok=True
#     )

#     print(
#         f"\nCREATING VECTORSTORE FOR {thread_id}"
#     )

#     db = Chroma.from_documents(

#         documents=chunks,

#         embedding=embedding_model,

#         persist_directory=persist_directory,

#         collection_name=collection_name
#     )

#     db.persist()

#     print(
#         "\nVECTORSTORE CREATED"
#     )

#     return db


# =========================================================
# LOAD VECTORSTORE
# =========================================================
def load_vectorstore(
    thread_id
):

    persist_directory = (
        f"{BASE_CHROMA_DIR}/{thread_id}"
    )

    collection_name = (
        f"collection_{thread_id}"
    )

    if not os.path.exists(
        persist_directory
    ):
        return None

    try:

        return Chroma(

            persist_directory=persist_directory,

            embedding_function=embedding_model,

            collection_name=collection_name
        )

    except Exception as e:

        print(
            f"LOAD FAILED: {e}"
        )

        return None