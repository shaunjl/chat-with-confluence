from langchain.document_loaders import ConfluenceLoader
from langchain.text_splitter import TokenTextSplitter
from langchain.vectorstores import Chroma

from utils.shared import get_embeddings_function, get_vector_store_persist_directory

def load_docs(confluence_space_key, confluence_url, confluence_username, confluence_api_key):
    loader = ConfluenceLoader(
        url=confluence_url,
        username=confluence_username,
        api_key=confluence_api_key
    )
    return loader.load(
        space_key=confluence_space_key, 
        limit=100
    ) # Maximum number of pages to retrieve per request, use max_pages to set Maximum number of pages to retrieve in total (defaults 1000)

def split_docs(documents):
    text_splitter = TokenTextSplitter(chunk_size=100, chunk_overlap=0)
    return text_splitter.split_documents(documents)

def store_docs_as_embeddings(docs, confluence_space_key):
    docs = split_docs(docs)

    Chroma.from_documents(
        documents=docs,
        embedding=get_embeddings_function(),
        persist_directory=get_vector_store_persist_directory(confluence_space_key)
    )

def process(confluence_space_key, confluence_url, confluence_username, confluence_api_key):
    docs = load_docs(
        confluence_space_key,
        confluence_url,
        confluence_username,
        confluence_api_key
    )

    store_docs_as_embeddings(
        docs,
        confluence_space_key
    )
