import os

from dotenv import load_dotenv

load_dotenv()

OPEN_AI_KEY = os.environ.get("OPEN_AI_KEY", default="my_api_key")

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", default="8578774376:AAEqM6QDggL")

POSTGRES_DB = os.environ.get("POSTGRES_DB", default="my_database_name")
POSTGRES_USER = os.environ.get("POSTGRES_USER", default="my_username")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", default="my_password")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", default="postgres")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", default="5432")

DATABASE_URL = (
    f"postgresql+asyncpg://{POSTGRES_USER}:" f"{POSTGRES_PASSWORD}@{POSTGRES_HOST}:" f"{POSTGRES_PORT}/{POSTGRES_DB}"
)
