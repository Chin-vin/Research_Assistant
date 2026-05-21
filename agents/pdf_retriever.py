from rag.retriever import (
    retrieve_documents
)


def pdf_retriever_agent(state):

    # -----------------------------
    # ROUTING MODE
    # -----------------------------

    mode = state.get(
        "routing",
        {}
    ).get(
        "retrieval_mode",
        "hybrid"
    )

    # -----------------------------
    # SKIP PDF RETRIEVAL
    # -----------------------------

    if mode not in [

        "pdf_only",

        "hybrid"
    ]:

        print(
            "\nSkipping PDF Retrieval"
        )

        return {

            "retrieved_docs": []
        }

    # -----------------------------
    # VECTOR DB
    # -----------------------------

    vector_db = state.get(
        "vector_db"
    )

    if not vector_db:

        print(
            "\nNo Vector DB Found"
        )

        return {

            "retrieved_docs":
                state.get(
                    "retrieved_docs",
                    []
                )
        }

    print(
        f"\nRunning PDF Retrieval "
        f"Mode: {mode}"
    )
    

    # -----------------------------
    # RETRIEVAL SETTINGS
    # -----------------------------

    TOP_K = 4

    if mode == "pdf_only":

        TOP_K = 8

    documents = []

    # -----------------------------
    # QUERY LOOP
    # -----------------------------
    queries = [state["query"]] + state["subqueries"]

    for query in queries:
   
        try:

            print(
                f"\nSearching PDF: "
                f"{query}"
            )

            results = retrieve_documents(

                vector_db,

                query,

                k=TOP_K
            )

            for doc in results:

                documents.append({

    "title": doc.metadata.get("source"),

    "content": doc.page_content,

    "page": doc.metadata.get("page"),

    "source": doc.metadata.get("source"),

    "url": doc.metadata.get("source")
})

        except Exception as e:

            print(
                f"PDF Retrieval Error: {e}"
            )

            continue

    # -----------------------------
    # COMBINE DOCUMENTS
    # -----------------------------

    existing_docs = state.get(
        "retrieved_docs",
        []
    )

    combined_docs = (
        existing_docs + documents
    )

    print(
        f"\nRetrieved PDF Docs: "
        f"{len(documents)}"
    )

    return {

        "retrieved_docs":
            combined_docs
    }