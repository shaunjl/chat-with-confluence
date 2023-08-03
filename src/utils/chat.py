import argparse
import os
import streamlit as st

from streamlit_chat import message

from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

from utils.shared import get_embeddings_function, get_vector_store_persist_directory

def get_vector_store(confluence_space_key):
    return Chroma(
        persist_directory=get_vector_store_persist_directory(confluence_space_key),
        embedding_function=get_embeddings_function()
    )

def run_chat_app(confluence_space_key):
    """Run the chat application using the Streamlit framework."""
    # Set the title for the Streamlit app
    st.title(f"Confluence Space {confluence_space_key} Chat")

    db = get_vector_store(confluence_space_key)

    # Initialize the session state for generated responses and past inputs
    if "generated" not in st.session_state:
        st.session_state["generated"] = ["How can I help you?"]

    if "past" not in st.session_state:
        st.session_state["past"] = ["Hello"]

    # Get the user's input from the text input field
    user_input = get_text()

    # If there is user input, search for a response using the search_db function
    if user_input:
        output = search_db(db, user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)

    # If there are generated responses, display the conversation using Streamlit
    # messages
    if st.session_state["generated"]:
        for i in range(len(st.session_state["generated"])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
            message(st.session_state["generated"][i], key=str(i))

def get_text():
    """Create a Streamlit input field and return the user's input."""
    input_text = st.text_input("input", key="input", label_visibility="hidden", placeholder="Ask me a question")
    return input_text

def search_db(db, query):
    """Search for a response to the query in the local Chroma database."""
    # Create a retriever from the Chroma instance
    retriever = db.as_retriever()
    # Set the search parameters for the retriever
    retriever.search_kwargs["distance_metric"] = "cos"
    retriever.search_kwargs["fetch_k"] = 100
    retriever.search_kwargs["maximal_marginal_relevance"] = True
    retriever.search_kwargs["k"] = 10
    # Create a ChatOpenAI model instance
    model = ChatOpenAI(model="gpt-3.5-turbo")
    # Create a RetrievalQA instance from the model and retriever
    qa = RetrievalQA.from_chain_type(model, retriever=retriever)
    # Return the result of the query
    return qa.run(query)

if __name__ == "__main__":
    os.environ['TOKENIZERS_PARALLELISM'] = 'false'
    parser = argparse.ArgumentParser()
    parser.add_argument("--confluence_space_key", type=str, required=True)
    args = parser.parse_args()

    run_chat_app(args.confluence_space_key)
