from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from backend.app.config import DATABASE_URL

# Engine — один на приложение
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # True — если хочешь видеть SQL в логах
    pool_pre_ping=True,
)

# Фабрика сессий
async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


# Dependency / helper
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
