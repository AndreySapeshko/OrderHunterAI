import asyncio
from types import SimpleNamespace

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from backend.app.config import POSTGRES_PASSWORD, POSTGRES_USER
from backend.app.db.base import Base
from backend.app.db.models.leads import Lead

TEST_DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/test_db"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture
def sessionmaker(engine):
    return async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
    )


@pytest_asyncio.fixture
async def session(sessionmaker) -> AsyncSession:
    async_session = sessionmaker
    async with async_session() as session:
        async with session.begin():
            yield session


@pytest.fixture
async def sample_lead(session):
    lead = Lead(title="AI chatbot for support", description="Need an AI chatbot using GPT for customer support")
    session.add(lead)
    await session.commit()
    await session.refresh(lead)
    return lead


@pytest.fixture
def lead():
    return SimpleNamespace(
        title="AI chatbot for customer support", description="Need an AI chatbot using GPT for support automation"
    )


@pytest.fixture
def lead_ai_good():
    return SimpleNamespace(score=85, category="chatbot")


@pytest.fixture
def lead_ai_bad_score():
    return SimpleNamespace(score=40, category="chatbot")


@pytest.fixture
def lead_ai_wrong_category():
    return SimpleNamespace(score=90, category="analytics")
