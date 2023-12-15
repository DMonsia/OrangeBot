from dotenv import dotenv_values

venv = dotenv_values(".env")

# Model metadata
OPENAI_API_KEY = venv.get("OPENAI_API_KEY")
CHAT_MODEL = "gpt-3.5-turbo"  # or "gpt-4-0314"

# csv metadata
METADATA_COLUMNS = ["Subject", "source", "Content"]
INDEXED_COLUMNS = "Content"
DATA_SOURCE = "Link"
CONTEXT_COLUMN = "Content"
CSV_SEP = ","

# vectorstore
STORE_FILE = "./data/vectorstore"
