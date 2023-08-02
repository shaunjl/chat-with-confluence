# 📖🔊 Chat With Confluence

# Overview
Use Embedded Vector Store and an LLM to chat with your Confluence docs

✨ Only need a Confluence Account and OpenAI account.

Uses (all via Langchain):
- Confluence API
- Hugging Face
- ChromaDB
- OpenAI

# Approach
1. Create a local embedding vector store of the Confluence docs
2. use the embedding vector store to get relevant texts from the store
3. provide the llm with the received texts + question as a prompt to answer the question

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
python3 -m pip install -r requirements.txt
```

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
The overall structure was pulled from [peterw/Chat-With-Github-Repo](https://github.com/peterw/Chat-with-Github-Repo)

# License

[MIT License](LICENSE)
