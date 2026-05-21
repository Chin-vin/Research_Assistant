from tools.tavily_tool import (
    tavily_search
)
from rag.ingestion import (
    ingest_documents_to_vectorstore
)

MAX_WEB_QUERIES = 5


def web_retriever_agent(state):

    # --------------------------------
    # ROUTING MODE
    # --------------------------------

    mode = state.get(
        "routing",
        {}
    ).get(
        "retrieval_mode",
        "hybrid"
    )
   
    # --------------------------------
    # SKIP WEB RETRIEVAL
    # --------------------------------

    if mode in [

        "pdf_only",

        "arxiv_only"
    ]:

        print(
            "\nSkipping Web Retrieval"
        )

        return {

            "retrieved_docs": []
        }

    # --------------------------------
    # RETRIEVAL SETTINGS
    # --------------------------------

    WEB_RESULTS = 3

    if mode == "web_only":

        WEB_RESULTS = 5

    documents = []

    subqueries = state.get(
        "subqueries",
        []
    )

    if not subqueries:

        return {

            "retrieved_docs":
                state.get(
                    "retrieved_docs",
                    []
                )
        }

    print(
        f"\nRunning Web Retrieval "
        f"Mode: {mode}"
    )

    # --------------------------------
    # QUERY LOOP
    # --------------------------------

    for query in subqueries[
        :MAX_WEB_QUERIES
    ]:

        try:

            print(
                f"\nSearching Tavily: "
                f"{query}"
            )

            results = tavily_search(
                query
            )

            if results:

                documents.extend(
                    results[:WEB_RESULTS]
                )

        except Exception as e:

            print(
                f"Web Retriever Error: {e}"
            )

            continue

    # --------------------------------
    # COMBINE DOCUMENTS
    # --------------------------------

    existing_docs = state.get(
        "retrieved_docs",
        []
    )

    combined_docs = (
        existing_docs + documents
    )
    # --------------------------------
    # VECTOR INGESTION
    # --------------------------------

    vector_db = state.get(
        "vector_db"
    )
    print("Combined docs")
    print(combined_docs)

    vector_db = ingest_documents_to_vectorstore(

        documents=documents,

        existing_vectorstore=vector_db
    )
    print(
        f"\nRetrieved Web Docs: "
        f"{len(documents)}"
    )

    return {

    "retrieved_docs":
        combined_docs,

    "vector_db":
        vector_db
}