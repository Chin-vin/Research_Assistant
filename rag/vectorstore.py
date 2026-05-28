
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
from langchain_community.vectorstores import Chroma
import os

from core.singletons import get_embeddings

embedding_model = get_embeddings()

# def create_vectorstore(
#     chunks,
#     thread_id
# ):
#     print("\n===== CREATE THREAD ID =====")
#     print(thread_id)
#     persist_directory = f"./chroma_db/{thread_id}"

#     os.makedirs(
#         persist_directory,
#         exist_ok=True
#     )

#     collection_name = f"collection_{thread_id}"

#     print("\nCREATE THREAD ID")
#     print(thread_id)

#     db = Chroma.from_documents(

#         documents=chunks,

#         embedding=embedding_model,

#         persist_directory=persist_directory,

#         collection_name=collection_name
#     )

#     db.persist()

#     print("\nVECTORSTORE CREATED")

#     print("Persist Dir:", persist_directory)

#     print("Collection:", collection_name)

#     print("Chunk Count:", len(chunks))

#     return db
import os
import shutil

from langchain_community.vectorstores import Chroma
from core.singletons import get_embeddings

embedding_model = get_embeddings()


# =========================================================
# CREATE VECTORSTORE
# =========================================================
def create_vectorstore(
    chunks,
    thread_id
):

    print("\n===== CREATE THREAD ID =====")
    print(thread_id)

    persist_directory = f"./chroma_db/{thread_id}"

    collection_name = f"collection_{thread_id}"

    # ==========================================
    # DELETE OLD VECTORSTORE
    # ==========================================
    if os.path.exists(persist_directory):

        print("\nOLD VECTORSTORE FOUND")
        print("DELETING OLD VECTORSTORE...")

        shutil.rmtree(
            persist_directory
        )

    # recreate folder
    os.makedirs(
        persist_directory,
        exist_ok=True
    )

    print("\nCREATING NEW VECTORSTORE...")

    db = Chroma.from_documents(

        documents=chunks,

        embedding=embedding_model,

        persist_directory=persist_directory,

        collection_name=collection_name
    )

    db.persist()

    print("\nVECTORSTORE CREATED")

    print("Persist Dir:", persist_directory)

    print("Collection:", collection_name)

    print("Chunk Count:", len(chunks))

    return db
# =========================================================
# LOAD VECTORSTORE
# =========================================================
def load_vectorstore(
    thread_id
):

    persist_directory = f"./chroma_db/{thread_id}"

    collection_name = f"collection_{thread_id}"

    print("\nLOAD THREAD ID")
    print(thread_id)

    if not os.path.exists(
        persist_directory
    ):

        print("VECTORSTORE DIRECTORY NOT FOUND")

        return None

    db = Chroma(

        persist_directory=persist_directory,

        embedding_function=embedding_model,

        collection_name=collection_name
    )

    try:

        count = db._collection.count()

        print(f"VECTORSTORE DOC COUNT: {count}")

    except Exception as e:

        print(str(e))

    return db


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