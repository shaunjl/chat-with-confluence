# 🛠️ this is still a work in progress 🛠️

# Overview
📖 Use Embedded Vector Store and an LLM to chat with your confluence docs

✨ Only need a Confluence Account and OpenAI account. Otherwise, uses only open source (Hugging Face, Chroma, LangChain)

# Approach
1. Create an embedding vector store of the Confluence docs
  - use [langchain.document_loaders.ConfluenceLoader](https://github.com/langchain-ai/langchain/blob/13b4f465e2e67451549dc0662495ae07b3530659/libs/langchain/langchain/document_loaders/confluence.py#L35) to load the Confluence docs
  - use [langchain.text_splitter.CharacterTextSplitter](https://github.com/langchain-ai/langchain/blob/c2d1d903fa35b91018b4d777db2b008fcbaa9fbc/langchain/text_splitter.py#L159) and [langchain.text_splitter.TokenTextSplitter](https://github.com/langchain-ai/langchain/blob/c2d1d903fa35b91018b4d777db2b008fcbaa9fbc/langchain/text_splitter.py#L177) to break up the docs into `documents` for processing
  - TODO: choose embedding vector store
2. use the embedding vector store to get relevant texts from the store
  - Create an embedding of the question (also using [langchain.embedddings.HuggingFaceEmbeddings](https://github.com/langchain-ai/langchain/blob/13b4f465e2e67451549dc0662495ae07b3530659/libs/langchain/langchain/embeddings/huggingface.py#L15))
  - Perform similarity search in the vector store using the question embedding to get relevant texts from the store
3. provide the llm with the received texts + question as a prompt to answer the question
  - Use [langchain.chat_modals.ChatOpenAI](https://github.com/langchain-ai/langchain/blob/master/libs/langchain/langchain/chat_models/openai.py#L181)
  - use [langchain.chains.RetrievalQA](https://github.com/langchain-ai/langchain/blob/13b4f465e2e67451549dc0662495ae07b3530659/libs/langchain/langchain/chains/retrieval_qa/base.py#L27)

# Usage
## 0. Pre-requisites
- Confluence API Key
- OpenAI account and API Key


## 1. Set up
### Create your `.env` file

```bash
cp .env.example .env
```

Set the values (don't worry, this file is in `.gitignore`)

### (Optional) Get in a virtual environment

```bash
python3 -m venv pyenv
source pyenv/bin/activate`
```

### Install python requirements
```bash
python3 -m pip3 install -r requirements.txt
```

(TODO: don't forget `python3 -m pip3 freeze > requirements.txt`)

## 2. Create your vector store ("process")
Use the `process` subcommand
Your confluence space key can be found in it's URL like `https://example.atlassian.net/wiki/spaces/<space-key>`

```bash
python3 src/main.py --confluence-space-key ABC process
```

> Note that subsequent runs with the same arguments will replace the previous vector store for that confluence space

## 3. Chat with your vector store ("chat")
To start the chat application using an existing dataset, use the `chat` subcommand:

```bash
python3 src/main.py --confluence-space-key ABC chat
```

The Streamlit chat app will run, and you can interact with the chatbot at `http://localhost:8501` (or the next available port) to ask questions about the repository.

## 4. (optional) Exit the virtual environment
```bash
deactivate
```

## Help
> For complete CLI instructions run `python src/main.py --help`

# Thanks to
The overall structure was inspired by [peterw/Chat-With-Github-Repo](https://github.com/peterw/Chat-with-Github-Repo)

# License

[MIT License](LICENSE)
