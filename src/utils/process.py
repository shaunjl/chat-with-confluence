import os

from langchain.document_loaders import ConfluenceLoader
from langchain.text_splitter import CharacterTextSplitter, TokenTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

# TODO - 4 spaces everywhere?
def load_docs(confluence_space_key, confluence_url, confluence_username, confluence_api_key):
    loader = ConfluenceLoader(
        url=confluence_url,
        username = confluence_username,
        api_key= confluence_api_key
    )
    return loader.load(
        space_key=confluence_space_key, 
        limit=100
    ) # Maximum number of pages to retrieve per request, use max_pages to set Maximum number of pages to retrieve in total (defaults 1000)

def split_docs(documents):
    # TODO - consult https://python.langchain.com/docs/modules/data_connection/document_transformers/text_splitters/split_by_token
    # text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    # texts = text_splitter.split_documents(documents)
    # text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=10) # TODO - encoding_name??
    # return text_splitter.split_documents(texts)
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    return text_splitter.split_documents(documents)


def get_embeddings_function():
    # TODO - validate configs
    model_name = "sentence-transformers/all-mpnet-base-v2"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

# TODO - which functions should go in a shared space?

def add_embeddings_to_store(texts):
  return Chroma.from_documents(
      documents=texts,
      embedding=get_embeddings_function(),
      persist_directory=persist_directory
  )

def get_vector_store_persist_directory(confluence_space_key):
  return os.path.join("./chroma_stores", confluence_space_key)

def store_docs_as_embeddings(docs, confluence_space_key):
    Chroma.from_documents(
        documents=split_docs(docs),
        embedding=get_embeddings_function(),
        persist_directory=get_vector_store_persist_directory(confluence_space_key)
    )

def process(confluence_space_key, confluence_url, confluence_username, confluence_api_key):
    """
    TODO - describe
    """
    docs = load_docs(
        confluence_space_key,
        confluence_url,
        confluence_username,
        confluence_api_key
    )

    print(f"Loaded {len(docs)} documents.")
    print(f"First document: {len(docs[0])}")

    store_docs_as_embeddings(
        docs,
        confluence_space_key
    )
