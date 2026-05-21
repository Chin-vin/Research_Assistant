
from langchain_community.vectorstores import (
    Chroma
)

from core.singletons import (
    get_embeddings
)

embedding_model = get_embeddings()

PERSIST_DIRECTORY = "./chroma_db"


def create_vectorstore(chunks):

    db = Chroma.from_documents(

        documents=chunks,

        embedding=embedding_model,

        persist_directory=
            PERSIST_DIRECTORY
    )

    db.persist()

    return db


def load_vectorstore():

    return Chroma(

        persist_directory=
            PERSIST_DIRECTORY,

        embedding_function=
            embedding_model
    )


