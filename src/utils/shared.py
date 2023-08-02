import os

from langchain.embeddings import HuggingFaceEmbeddings

def get_embeddings_function():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': False}
    )

def get_vector_store_persist_directory(confluence_space_key):
    return os.path.join("./chroma_stores", confluence_space_key)