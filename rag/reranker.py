from core.singletons import (
    get_reranker
)

reranker = get_reranker()

def rerank_documents(

    query,

    documents,

    top_k=8
):

    pairs = [

        (query, doc.get(
    "content",
    ""
))

        for doc in documents
    ]

    scores = reranker.predict(
        pairs
    )

    ranked = sorted(

        zip(scores, documents),

        key=lambda x: x[0],

        reverse=True
    )

    return [

        doc

        for score, doc in ranked[:top_k]
    ]