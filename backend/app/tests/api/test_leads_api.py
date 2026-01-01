from datetime import datetime

import pytest
from httpx import ASGITransport, AsyncClient

from backend.app.api.main import app
from backend.app.db import Lead, LeadAI, RawItem, UserLead


@pytest.mark.asyncio
async def test_get_leads(sessionmaker, monkeypatch):
    monkeypatch.setattr("backend.app.api.routers.leads.async_session", sessionmaker)
    transport = ASGITransport(app=app)
    async with AsyncClient(base_url="http://test", transport=transport) as client:
        resp = await client.get("/api/leads/")

    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.asyncio
async def test_get_user_leads(sessionmaker, monkeypatch):
    monkeypatch.setattr("backend.app.api.routers.user_leads.async_session", sessionmaker)
    transport = ASGITransport(app=app)
    async with AsyncClient(base_url="http://test", transport=transport) as client:
        resp = await client.get("/api/user_leads/")

    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.asyncio
async def test_get_raw_items(sessionmaker, monkeypatch):
    monkeypatch.setattr("backend.app.api.routers.raw_items.async_session", sessionmaker)
    transport = ASGITransport(app=app)
    async with AsyncClient(base_url="http://test", transport=transport) as client:
        resp = await client.get("/api/raw_items/")

    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.asyncio
async def test_get_lead_by_id(session, sessionmaker, monkeypatch):
    monkeypatch.setattr("backend.app.api.routers.leads.async_session", sessionmaker)
    raw = RawItem(
        source_id="kwork_projects",
        title="AI chatbot for support",
        content="Need an AI chatbot using GPT for customer support",
    )
    session.add(raw)
    await session.flush()
    lead = Lead(raw_item_id=raw.id)
    session.add(lead)
    await session.flush()
    lead_ai = LeadAI(lead_id=lead.id, category="bot", is_relevant=True, score=70, extracted={})
    session.add(lead_ai)
    await session.commit()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get(f"/api/leads/{lead.id}")

    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == str(lead.id)


@pytest.mark.asyncio
async def test_get_user_lead_by_id(session, sessionmaker, test_user, monkeypatch):
    monkeypatch.setattr("backend.app.api.routers.user_leads.async_session", sessionmaker)
    raw = RawItem(
        source_id="kwork_projects",
        title="AI chatbot for support",
        content="Need an AI chatbot using GPT for customer support",
        published_at=datetime.utcnow(),
        external_id="external_id",
        url="http://test.com",
        author="test author",
    )
    session.add(raw)
    await session.flush()
    lead = Lead(raw_item_id=raw.id)
    session.add(lead)
    await session.flush()
    user_lead = UserLead(lead_id=lead.id, user_id=test_user.id)
    session.add(user_lead)
    await session.commit()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get(f"/api/user_leads/{user_lead.id}")

    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == str(user_lead.id)


# @pytest.mark.asyncio
# async def test_update_lead_status(session, sessionmaker, monkeypatch):
#     monkeypatch.setattr("backend.app.api.routers.leads.async_session", sessionmaker)
#     raw = RawItem(
#         source_id="kwork_projects",
#         title="AI chatbot for support",
#         content="Need an AI chatbot using GPT for customer support"
#     )
#     lead = Lead(raw_item_id=raw.id)
#     lead_ai = LeadAI(lead_id=lead.id, is_relevant=True, score=70)
#     session.add(lead, lead_ai)
#     await session.commit()
#
#     transport = ASGITransport(app=app)
#     async with AsyncClient(transport=transport, base_url="http://test") as client:
#         resp = await client.patch(
#             f"/api/leads/{lead.id}/status",
#             json={"status": "saved"},
#         )
#
#     assert resp.status_code == 200
#     assert resp.json()["status"] == "saved"
