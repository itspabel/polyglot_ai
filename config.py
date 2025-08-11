import os

FERNET_KEY = os.environ["FERNET_KEY"]
DB_PATH = os.environ.get("POLYGLOT_DB", "sqlite:///data/database.db")
