import argparse
import os
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
import streamlit as st
from streamlit_chat import message

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

def get_vector_store_persist_directory(confluence_space_key):
  return os.path.join("./chroma_stores", confluence_space_key)

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


def generate_response(prompt):
    """
    Generate a response using OpenAI's ChatCompletion API and the specified prompt.
    """
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )
    response = completion.choices[0].message.content
    return response


def get_text():
    """Create a Streamlit input field and return the user's input."""
    input_text = st.text_input("input", key="input", label_visibility="hidden", placeholder="Ask me a question")
    return input_text

def get_prompt():
    prompt_template = """Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    If the question isn't about the context, just say that your purpose is to provide information about the Confluence Space.

    {context}

    Question: {question}
    """
    return PromptTemplate(template=prompt_template, input_variables=["context", "question"])

def search_db(db, query):
    # TODO - see https://python.langchain.com/docs/integrations/vectorstores/chroma
    """Search for a response to the query in the DeepLake database."""
    # Create a retriever from the DeepLake instance
    retriever = db.as_retriever()
    # Set the search parameters for the retriever
    retriever.search_kwargs["distance_metric"] = "cos"
    retriever.search_kwargs["fetch_k"] = 100
    retriever.search_kwargs["maximal_marginal_relevance"] = True
    retriever.search_kwargs["k"] = 10
    # Create a ChatOpenAI model instance
    model = ChatOpenAI(model="gpt-3.5-turbo")
    # Create a RetrievalQA instance from the model and retriever
    chain_type_kwargs = {"prompt": get_prompt()}
    qa = RetrievalQA.from_chain_type(model, retriever=retriever, chain_type_kwargs=chain_type_kwargs)
    # Return the result of the query
    return qa.run(query)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--confluence_space_key", type=str, required=True)
    args = parser.parse_args()

    run_chat_app(args.confluence_space_key)
