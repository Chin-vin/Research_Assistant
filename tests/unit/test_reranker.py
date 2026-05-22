# # =========================================================
# # tests/unit/test_reranker.py
# # =========================================================

# from rag.reranker import (
#     rerank_documents
# )


# def test_reranking():

#     docs = [

#         {

#             "content":
#                 "AI improves healthcare."
#         },

#         {

#             "content":
#                 "Blockchain security."
#         }
#     ]

#     ranked = rerank_documents(

#         query="AI healthcare",

#         documents=docs,

#         top_k=1
#     )

#     assert len(ranked) == 1

# =========================================================
# tests/unit/test_reranker.py
# =========================================================

from rag.reranker import (
    rerank_documents
)


class MockDocument:

    def __init__(self, content):

        self.page_content = content


def test_reranking():

    docs = [

        MockDocument(
            "AI improves healthcare."
        ),

        MockDocument(
            "Blockchain security."
        )
    ]

    ranked = rerank_documents(

        query="AI healthcare",

        documents=docs,

        top_k=1
    )

    assert len(ranked) == 1

    assert (
        ranked[0].page_content
        ==
        "AI improves healthcare."
    )