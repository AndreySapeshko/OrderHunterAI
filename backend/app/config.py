import os

from dotenv import load_dotenv

load_dotenv()

OPEN_AI_KEY = os.environ["OPEN_AI_KEY"]

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

POSTGRES_DB = os.environ["POSTGRES_DB"]
POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_HOST = os.environ["POSTGRES_HOST"]
POSTGRES_PORT = os.environ["POSTGRES_PORT"]

DATABASE_URL = (
    f"postgresql+asyncpg://{POSTGRES_USER}:" f"{POSTGRES_PASSWORD}@{POSTGRES_HOST}:" f"{POSTGRES_PORT}/{POSTGRES_DB}"
)
