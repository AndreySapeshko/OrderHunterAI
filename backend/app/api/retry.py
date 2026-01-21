import asyncio

from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from backend.app.db.session import engine


async def wait_for_db(retries=10, delay=2):
    for i in range(retries):
        try:
            async with engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
            return
        except OperationalError:
            await asyncio.sleep(delay)
    raise RuntimeError("Database not available")
