# config/settings.py
#pip install python-dotenv
import os
from dotenv import load_dotenv
import json


load_dotenv()

REQUIRED_ENV_VARS = [
    "DB_HOST", "DB_PORT", "DB_USER", "DB_PASSWORD", "DB_DATABASE",
    "TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_IDS", "LINE_ACCESS_TOKEN", "LINE_RECIPIENT_IDS"
]

for var in REQUIRED_ENV_VARS:
    if not os.getenv(var):
        raise EnvironmentError(f"Missing environment variable: {var}")

# แยกตัวแปรออกมาให้ import ได้โดยตรง
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_DATABASE")

DB_CONFIG = {
    'host': DB_HOST,
    'port': DB_PORT,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'database': DB_NAME
}

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_IDS = json.loads(os.getenv("TELEGRAM_CHAT_IDS", "{}"))

LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
LINE_RECIPIENT_IDS = json.loads(os.getenv("LINE_RECIPIENT_IDS", "{}"))