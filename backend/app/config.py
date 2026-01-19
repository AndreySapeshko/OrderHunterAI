import os

from dotenv import load_dotenv

load_dotenv()

OPEN_AI_KEY = os.environ.get("OPEN_AI_KEY", default="my_api_key")
OPEN_ROUTER_URL = os.environ.get("OPEN_ROUTER_URL", default="https://openrouter.ai/api/v1")
OPEN_ROUTER_KEY = os.environ.get("OPEN_ROUTER_KEY", default="my_api_key")

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", default="my_telegram_bot_token")
TELEGRAM_API_ID = os.environ.get("TELEGRAM_API_ID", default="my_telegram_api_id")
TELEGRAM_API_HASH = os.environ.get("TELEGRAM_API_HASH", default="my_telegram_api_hash")
TELEGRAM_CHANNELS = os.environ.get("TELEGRAM_CHANNELS", default="")

TELETHON_SESSION_STRING = os.environ.get("TELETHON_SESSION_STRING", default="my_telethon_session_string")

POSTGRES_DB = os.environ.get("POSTGRES_DB", default="my_database_name")
POSTGRES_USER = os.environ.get("POSTGRES_USER", default="my_username")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", default="my_password")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", default="postgres")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", default="5432")

DATABASE_URL = (
    f"postgresql+asyncpg://{POSTGRES_USER}:" f"{POSTGRES_PASSWORD}@{POSTGRES_HOST}:" f"{POSTGRES_PORT}/{POSTGRES_DB}"
)
DATABASE_URL_SYNC = (
    f"postgresql+psycopg://{POSTGRES_USER}:" f"{POSTGRES_PASSWORD}@{POSTGRES_HOST}:" f"{POSTGRES_PORT}/{POSTGRES_DB}"
)

ENABLE_LLM_ANALYSIS = os.environ.get("ENABLE_LLM_ANALYSIS", default="True") == "True"
