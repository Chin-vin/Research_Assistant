
# from langchain_huggingface import (
#     HuggingFaceEmbeddings
# )

# embedding_model = (
#     HuggingFaceEmbeddings(

#         model_name=
#         "sentence-transformers/all-MiniLM-L6-v2"
#     )
# )
from core.singletons import (
    get_embeddings
)

embedding_model = get_embeddings()