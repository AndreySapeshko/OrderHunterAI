import pytest

from sqlalchemy import select

from backend.app.db.models.lead_ai import LeadAI
from backend.app.db.models.leads import Lead
from backend.app.llm.analyzer import LeadAnalyzer
from backend.app.tests.mocks.fake_llm import FakeLLMClient


@pytest.mark.asyncio
async def test_lead_analyzer_ai_lead(session, sessionmaker, monkeypatch):
    monkeypatch.setattr("backend.app.llm.analyzer.async_session", sessionmaker)
    fake_response = {
        "is_relevant": True,
        "relevance_reason": "AI chatbot project",
        "category": "chatbot",
        "requirements": {"type": "customer support"},
        "stack": ["Python", "OpenAI"],
        "budget": {"min": 1000, "max": 3000, "currency": "USD"},
        "deadline_days": 14,
        "score": 85,
    }

    llm = FakeLLMClient(fake_response)
    analyzer = LeadAnalyzer(llm_client=llm, prompt_version="v1")

    lead = Lead(title="AI chatbot for support", description="Need an AI chatbot using GPT for customer support")
    session.add(lead)
    await session.commit()

    await analyzer.analyze(lead)

    async with sessionmaker() as session:
        ai = await session.scalar(select(LeadAI).where(LeadAI.lead_id == lead.id))
    assert ai is not None
    assert ai.is_relevant is True
    assert ai.category == "chatbot"
    assert ai.score == 85
    assert ai.model == "fake-model"
    assert ai.prompt_version == "v1"


@pytest.mark.asyncio
async def test_lead_analyzer_not_ai(session, sessionmaker, monkeypatch):
    monkeypatch.setattr("backend.app.llm.analyzer.async_session", sessionmaker)
    fake_response = {
        "is_relevant": False,
        "relevance_reason": "Non-AI project",
        "category": "not_ai",
        "requirements": {},
        "stack": [],
        "budget": None,
        "deadline_days": None,
        "score": 10,
    }

    llm = FakeLLMClient(fake_response)
    analyzer = LeadAnalyzer(llm_client=llm, prompt_version="v1")

    lead = Lead(title="AI chatbot for support", description="Need an AI chatbot using GPT for customer support")
    session.add(lead)
    await session.commit()

    await analyzer.analyze(lead)

    async with sessionmaker() as session:
        ai = await session.scalar(select(LeadAI).where(LeadAI.lead_id == lead.id))

    assert ai.is_relevant is False
    assert ai.category == "not_ai"
    assert ai.score < 20


@pytest.mark.asyncio
async def test_lead_analyzer_idempotent(session, sessionmaker, monkeypatch):
    monkeypatch.setattr("backend.app.llm.analyzer.async_session", sessionmaker)
    llm1 = FakeLLMClient(
        {
            "is_relevant": True,
            "relevance_reason": "AI",
            "category": "chatbot",
            "requirements": {},
            "stack": [],
            "budget": None,
            "deadline_days": None,
            "score": 60,
        }
    )

    llm2 = FakeLLMClient(
        {
            "is_relevant": True,
            "relevance_reason": "AI refined",
            "category": "chatbot",
            "requirements": {},
            "stack": [],
            "budget": None,
            "deadline_days": None,
            "score": 80,
        }
    )

    analyzer1 = LeadAnalyzer(llm1, prompt_version="v1")
    analyzer2 = LeadAnalyzer(llm2, prompt_version="v1")

    lead = Lead(title="AI chatbot for support", description="Need an AI chatbot using GPT for customer support")
    session.add(lead)
    await session.commit()

    await analyzer1.analyze(lead)
    await analyzer2.analyze(lead)

    async with sessionmaker() as session:
        ai = await session.scalar(select(LeadAI).where(LeadAI.lead_id == lead.id))

    assert ai.score == 80


@pytest.mark.asyncio
async def test_lead_analyzer_invalid_json(session, sessionmaker, monkeypatch):
    monkeypatch.setattr("backend.app.llm.analyzer.async_session", sessionmaker)
    llm = FakeLLMClient(
        {
            "is_relevant": True,
            # category missing
            "score": 50,
        }
    )

    analyzer = LeadAnalyzer(llm, prompt_version="v1")

    lead = Lead(title="AI chatbot for support", description="Need an AI chatbot using GPT for customer support")
    session.add(lead)
    await session.commit()

    assert await analyzer.analyze(lead) is False
