from langchain_core.documents import (
    Document
)

from rag.chunking import (
    create_chunks
)

from rag.vectorstore import (
    create_vectorstore
)

def ingest_documents_to_vectorstore(

    documents,

    existing_vectorstore=None
):

    try:

        # --------------------------------
        # CONVERT TO LANGCHAIN DOCS
        # --------------------------------

        langchain_docs = []

        for doc in documents:

            langchain_docs.append(

                Document(

                    page_content=doc.get(
                        "content",
                        ""
                    ),

                    metadata={

                        "title":
                            doc.get(
                                "title",
                                ""
                            ),

                        "url":
                            doc.get(
                                "url",
                                ""
                            ),

                        "source":
                            doc.get(
                                "source",
                                ""
                            ),

                        "page":
                            doc.get(
                                "page",
                                ""
                            )
                    }
                )
            )

        # --------------------------------
        # CHUNKING
        # --------------------------------

        chunks = create_chunks(
            langchain_docs
        )

        print(
            f"\nGenerated Chunks: "
            f"{len(chunks)}"
        )

        # --------------------------------
        # VECTORSTORE
        # --------------------------------

        if existing_vectorstore:

            existing_vectorstore.add_documents(
                chunks
            )

            return existing_vectorstore

        return create_vectorstore(
            chunks
        )

    except Exception as e:

        print(
            f"\nVector Ingestion Error: "
            f"{str(e)}"
        )

        return existing_vectorstore