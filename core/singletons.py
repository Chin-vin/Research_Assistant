import streamlit as st

from sentence_transformers import (
    SentenceTransformer
)

from langchain_huggingface import (
    HuggingFaceEmbeddings
)

from langchain_groq import (
    ChatGroq
)

from sentence_transformers import (
    CrossEncoder
)

# =========================================================
# EMBEDDINGS SINGLETON
# =========================================================

@st.cache_resource
def get_embeddings():

    print(
        "Loading Embedding Model..."
    )

    return HuggingFaceEmbeddings(

        model_name=(
            "sentence-transformers/"
            "all-MiniLM-L6-v2"
        )
    )

# =========================================================
# SENTENCE TRANSFORMER
# =========================================================

@st.cache_resource
def get_sentence_transformer():

    print(
        "Loading Sentence Transformer..."
    )

    return SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

# =========================================================
# RERANKER
# =========================================================

@st.cache_resource
def get_reranker():

    print(
        "Loading Cross Encoder..."
    )

    return CrossEncoder(
        "cross-encoder/ms-marco-MiniLM-L-6-v2"
    )

# =========================================================
# FAST LLM
# =========================================================

@st.cache_resource
def get_fast_llm():

    print(
        "Loading Fast LLM..."
    )

    return ChatGroq(

        model="llama-3.3-70b-versatile",

        temperature=0
    )

# =========================================================
# REASONING LLM
# =========================================================

@st.cache_resource
def get_reasoning_llm():

    print(
        "Loading Reasoning LLM..."
    )

    return ChatGroq(

        model="qwen/qwen3-32b",

        temperature=0,
        streaming = True
    )