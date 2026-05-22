from tools.arxiv_tool import (
    search_arxiv
)
from rag.ingestion import (
    ingest_documents_to_vectorstore
)
from utils.query_validator import (
    is_valid_query
)

MAX_ARXIV_QUERIES = 5


def clean_query(query: str) -> str:

    """
    Cleans malformed LLM outputs before
    sending queries to arXiv.
    """

    bad_patterns = [

        "Here are",

        "Subtopics",

        "subqueries",

        "Subqueries",

        "Research Topics",

        "Topics",

        "*",

        "#",

        ":",

        "[",
        "]",

        "{",
        "}",

        "```",

        "\"",

        "'"
    ]

    for pattern in bad_patterns:

        query = query.replace(
            pattern,
            ""
        )

    query = " ".join(query.split())

    return query.strip()


def arxiv_retriever_agent(state):

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
    # SKIP ARXIV RETRIEVAL
    # --------------------------------

    if mode == "pdf_only":

        print(
            "\nSkipping Arxiv Retrieval"
        )

        return {

            "retrieved_docs": []
        }

    # --------------------------------
    # RETRIEVAL SETTINGS
    # --------------------------------

    ARXIV_RESULTS = 2

    if mode == "arxiv_only":

        ARXIV_RESULTS = 5

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
        f"\nRunning Arxiv Retrieval "
        f"Mode: {mode}"
    )
    
    # --------------------------------
    # QUERY LOOP
    # --------------------------------

    for query in subqueries[
        :MAX_ARXIV_QUERIES
    ]:

        try:

            cleaned_query = clean_query(
                query
            )

            if not is_valid_query(
                cleaned_query
            ):

                print(
                    f"Skipping invalid query: "
                    f"{cleaned_query}"
                )

                continue

            print(
                f"Searching Arxiv: "
                f"{cleaned_query}"
            )

            results = search_arxiv(
                cleaned_query
            )

            if results:

                documents.extend(
                    results[:ARXIV_RESULTS]
                )

        except Exception as e:

            print(
                f"Arxiv Retriever Error: {e}"
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
    vector_db = state.get(
        "vector_db"
    )

    vector_db = ingest_documents_to_vectorstore(

    documents=documents,

    thread_id=state["thread_id"],

    existing_vectorstore=vector_db
)

    print(
        f"\nRetrieved Arxiv Docs: "
        f"{len(documents)}"
    )

    return {

    "retrieved_docs":
        combined_docs,

    "vector_db":
        vector_db
}