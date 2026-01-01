import asyncio
from types import SimpleNamespace
from uuid import uuid4

import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from backend.app.config import POSTGRES_PASSWORD, POSTGRES_USER
from backend.app.db import RawItem, User, UserLead
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
        await conn.execute(text("DROP SCHEMA public CASCADE"))
        await conn.execute(text("CREATE SCHEMA public"))
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
async def test_user(session):
    user = User(chat_id=1234, password="pass123", email="test@tester.ru")
    session.add(user)
    await session.flush()
    await session.refresh(user)
    return user


@pytest.fixture
async def raw_item(session):
    raw = RawItem(source_id="test_source", title="Test title", content="Test description")
    session.add(raw)
    await session.flush()
    await session.refresh(raw)
    return raw


@pytest.fixture
async def lead(session, raw_item):
    lead = Lead(raw_item_id=raw_item.id)
    session.add(lead)
    await session.flush()
    await session.refresh(lead)
    return lead


@pytest.fixture
async def user_lead(test_user, lead, session):
    user_lead = UserLead(user_id=test_user.id, lead_id=lead.id)
    session.add(user_lead)
    await session.flush()
    await session.refresh(user_lead)
    return user_lead


@pytest.fixture
def lead_ai_good():
    return SimpleNamespace(score=85, category="chatbot")


@pytest.fixture
def lead_ai_bad_score():
    return SimpleNamespace(score=40, category="chatbot")


@pytest.fixture
def lead_ai_wrong_category():
    return SimpleNamespace(score=90, category="analytics")


@pytest.fixture
def simple_lead():
    return SimpleNamespace(id=uuid4(), raw_item_id=uuid4())


@pytest.fixture
def lead_ai_relevant():
    return SimpleNamespace(is_relevant=True, score=80, category="chatbot")


@pytest.fixture
def lead_ai_not_relevant():
    return SimpleNamespace(is_relevant=False, score=10, category="not_ai")


@pytest.fixture
def user():
    return SimpleNamespace(id=uuid4(), chat_id=123456, is_active=True)


@pytest.fixture
def rule():
    return SimpleNamespace(enabled=True)
