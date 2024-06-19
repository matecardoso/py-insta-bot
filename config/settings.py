from dotenv import load_dotenv, find_dotenv
import os

dotenv_path = find_dotenv()
if not dotenv_path:
    raise FileNotFoundError("Arquivo .env não encontrado")
load_dotenv(dotenv_path)

INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")
INSTAGRAM_BACKUP_CODES = os.getenv("INSTAGRAM_BACKUP_CODES").strip("[]").replace("\"", "").split(",")
