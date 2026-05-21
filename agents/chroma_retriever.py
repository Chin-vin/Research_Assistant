from rag.retriever import retrieve_documents


def chroma_retriever_agent(state):

    db = state["vector_db"]

    documents = []

    for query in state["subqueries"]:

        results = retrieve_documents(
            db,
            query
        )

        for doc in results:

            documents.append({
                "content": doc.page_content,
                "metadata": doc.metadata
            })

    existing_docs = state.get(
        "retrieved_docs",
        []
    )

    return {
        "retrieved_docs": (
            existing_docs + documents
        )
    }