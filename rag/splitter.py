from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

def split_documents(documents):

    splitter = (
        RecursiveCharacterTextSplitter(

            chunk_size=1200,

            chunk_overlap=250
        )
    )

    return splitter.split_documents(
        documents
    )

# ----------------------------------------
# OPTIONAL ALIAS
# ----------------------------------------

create_chunks = split_documents
