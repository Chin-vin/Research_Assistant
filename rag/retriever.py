
from rag.semantic_search import (
    semantic_search
)

from rag.reranker import (
    rerank_documents
)

# =========================================================
# MAIN RAG RETRIEVER
# =========================================================

def retrieve_documents(

    vector_db,

    query,

    k=15,

    rerank_top_k=8
):

    try:

        print(
            "\n========== RAG RETRIEVAL ==========\n"
        )

        print(
            f"Query: {query}"
        )

        # -------------------------------------------------
        # VECTOR DB CHECK
        # -------------------------------------------------

        if not vector_db:

            print(
                "\nNo Vector DB Found"
            )

            return []

        # -------------------------------------------------
        # SEMANTIC SEARCH
        # -------------------------------------------------

        print(
            "\nRunning Semantic Search..."
        )

        semantic_results = semantic_search(

            vector_db=vector_db,

            query=query,

            k=k
        )

        print(
            f"Semantic Results: "
            f"{len(semantic_results)}"
        )

        if not semantic_results:

            print(
                "\nNo Semantic Results Found"
            )

            return []

        # -------------------------------------------------
        # CONVERT DOCS
        # -------------------------------------------------

        documents = []

        for doc in semantic_results:

            documents.append({

                "title":
                    doc.metadata.get(
                        "title",

                        doc.metadata.get(
                            "source",
                            "Unknown Source"
                        )
                    ),

                "content":
                    doc.page_content,

                "url":
                    doc.metadata.get(
                        "url",

                        doc.metadata.get(
                            "source",
                            "No URL"
                        )
                    ),

                "source":
                    doc.metadata.get(
                        "source",
                        ""
                    ),

                "page":
                    doc.metadata.get(
                        "page",
                        ""
                    )
            })

        # -------------------------------------------------
        # RERANKING
        # -------------------------------------------------

        print(
            "\nRunning Reranking..."
        )

        reranked_docs = rerank_documents(

            query=query,

            documents=documents,

            top_k=rerank_top_k
        )

        print(
            f"Reranked Results: "
            f"{len(reranked_docs)}"
        )

        # -------------------------------------------------
        # REMOVE DUPLICATES
        # -------------------------------------------------

        unique_docs = []

        seen = set()

        for doc in reranked_docs:

            content = doc.get(
                "content",
                ""
            )

            if content not in seen:

                seen.add(content)

                unique_docs.append(doc)

        print(
            f"Unique Results: "
            f"{len(unique_docs)}"
        )

        # -------------------------------------------------
        # FINAL DEBUG
        # -------------------------------------------------

        print(
            "\n========== FINAL RETRIEVED DOCS ==========\n"
        )

        for idx, doc in enumerate(unique_docs):

            print(
                f"\nDocument {idx + 1}"
            )

            print(
                f"Title: "
                f"{doc.get('title')}"
            )

            print(
                f"URL: "
                f"{doc.get('url')}"
            )

            print(
                f"Content Preview: "
                f"{doc.get('content')[:300]}"
            )

        return unique_docs

    except Exception as e:

        print(
            f"\nRetriever Error: "
            f"{str(e)}"
        )

        return [] 
