from rag.loader import load_pdf

from rag.splitter import (
    split_documents
)

from rag.vectorstore import (
    create_vectorstore
)


def process_pdf(file_path):

    docs = load_pdf(file_path)

    chunks = split_documents(docs)

    vector_db = create_vectorstore(
        chunks
    )

    return vector_db