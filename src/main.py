import argparse
import os
import sys
from dotenv import load_dotenv
from streamlit.web import cli as stcli
from utils.process import process

# Load environment variables from a .env file
load_dotenv()

def process_docs(args):
    """
    Process a Confluence space and store the results in Bedrock
    """
    process(
      args.confluence_space_key,
      os.environ.get("CONFLUENCE_URL"),
      os.environ.get("CONFLUENCE_USERNAME"),
      os.environ.get("CONFLUENCE_API_KEY")
    )

def chat(args):
    """
    Start the Streamlit chat application using the local Chroma dataset for the specified Confluence space
    """

    sys.argv = [
        "streamlit",
        "run",
        "src/utils/chat.py",
        "--",
        f"--confluence_space_key={args.confluence_space_key}",
    ]

    sys.exit(stcli.main())

def main():
    """Define and parse CLI arguments, then execute the appropriate subcommand."""
    parser = argparse.ArgumentParser(description="Chat with Confluence Docs")
    parser.add_argument(
        "--confluence-space-key", required=True, help="Confluence space key"
    )
    subparsers = parser.add_subparsers(dest="command")

    # Process subcommand
    process_parser = subparsers.add_parser("process", help="Process a Confluence space")

    # Chat subcommand
    chat_parser = subparsers.add_parser("chat", help="Start the chat application")

    args = parser.parse_args()

    if args.command == "process":
        process_docs(args)
    elif args.command == "chat":
        chat(args)

if __name__ == "__main__":
    main()
