
# from langchain_community.vectorstores import (
#     Chroma
# )

# from core.singletons import (
#     get_embeddings
# )

# embedding_model = get_embeddings()

# PERSIST_DIRECTORY = "./chroma_db"


# def create_vectorstore(chunks):

#     db = Chroma.from_documents(

#         documents=chunks,

#         embedding=embedding_model,

#         persist_directory=
#             PERSIST_DIRECTORY
#     )

#     db.persist()

#     return db


# def load_vectorstore():

#     return Chroma(

#         persist_directory=
#             PERSIST_DIRECTORY,

#         embedding_function=
#             embedding_model
#     )


import os

from langchain_community.vectorstores import (
    Chroma
)

from core.singletons import (
    get_embeddings
)

embedding_model = get_embeddings()


# =========================================================
# CREATE VECTORSTORE
# =========================================================

def create_vectorstore(

    chunks,

    thread_id
):

    persist_directory = (
        f"./chroma_db/{thread_id}"
    )

    os.makedirs(
        persist_directory,
        exist_ok=True
    )

    db = Chroma.from_documents(

        documents=chunks,

        embedding=embedding_model,

        persist_directory=persist_directory
    )

    db.persist()

    return db


# =========================================================
# LOAD VECTORSTORE
# =========================================================

def load_vectorstore(

    thread_id
):

    persist_directory = (
        f"./chroma_db/{thread_id}"
    )

    return Chroma(

        persist_directory=
            persist_directory,

        embedding_function=
            embedding_model
    )


# =========================================================
# DELETE VECTORSTORE
# =========================================================

def delete_vectorstore(

    thread_id
):

    persist_directory = (
        f"./chroma_db/{thread_id}"
    )

    if os.path.exists(
        persist_directory
    ):

        import shutil

        shutil.rmtree(
            persist_directory
        )