from rag.retriever import (
    retrieve_documents
)

from models.llm_registry import (
    fast_llm
)


def chat_with_report(

    vector_db,

    query
):

    # =====================================
    # RETRIEVE RELEVANT CHUNKS
    # =====================================

    docs = retrieve_documents(

        vector_db=vector_db,

        query=query,

        k=6,

        rerank_top_k=4
    )

    # =====================================
    # NO RESULTS
    # =====================================

    if not docs:

        return (
            "No relevant information "
            "found in uploaded PDFs."
        )

    # =====================================
    # BUILD CONTEXT
    # =====================================

    context = ""

    for idx, doc in enumerate(docs):

        title = doc.get(
            "title",
            f"Document {idx+1}"
        )

        source = doc.get(
            "url",
            "Unknown Source"
        )

        content = doc.get(
            "content",
            ""
        )

        context += f"""

DOCUMENT {idx+1}

TITLE:
{title}

SOURCE:
{source}

CONTENT:
{content}

"""

    # =====================================
    # PROMPT
    # =====================================

    prompt = f"""

You are an intelligent assistant.

Answer the user's question naturally
and directly using the provided context.

IMPORTANT RULES:

- Give concise human-like answers
- Summarize information naturally
- Combine ideas intelligently
- Avoid robotic phrasing
- Avoid mentioning:
    - PDFs
    - documents
    - retrieved content
    - sources
    - studies
    - "the uploaded PDFs"
    - "the document contains"
    - "the research mentions"

- Do NOT explain where information came from
- Just provide the answer directly

If information is insufficient, say:

"Insufficient information available."

CONTEXT:
{context}

QUESTION:
{query}

Generate a concise,
natural,
well-structured answer.

"""
    response = fast_llm.invoke(
        prompt
    )

    return response.content