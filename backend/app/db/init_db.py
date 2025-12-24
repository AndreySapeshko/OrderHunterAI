import asyncio

from backend.app.db.base import Base
from backend.app.db.session import engine
import backend.app.db.__init__


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(init_models())
