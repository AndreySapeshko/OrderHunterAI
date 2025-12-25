import pytest
from httpx import ASGITransport, AsyncClient

from backend.app.api.main import app
from backend.app.db import Lead, LeadAI


@pytest.mark.asyncio
async def test_get_leads(sessionmaker, monkeypatch):
    monkeypatch.setattr("backend.app.api.routers.leads.async_session", sessionmaker)
    transport = ASGITransport(app=app)
    async with AsyncClient(base_url="http://test", transport=transport) as client:
        resp = await client.get("/api/leads/")

    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.asyncio
async def test_get_lead_by_id(session, sessionmaker, monkeypatch):
    monkeypatch.setattr("backend.app.api.routers.leads.async_session", sessionmaker)
    lead = Lead(title="AI chatbot for support", description="Need an AI chatbot using GPT for customer support")
    lead_ai = LeadAI(lead_id=lead.id, is_relevant=True, score=70)
    session.add(lead, lead_ai)
    await session.commit()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get(f"/api/leads/{lead.id}")

    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == str(lead.id)


@pytest.mark.asyncio
async def test_update_lead_status(session, sessionmaker, monkeypatch):
    monkeypatch.setattr("backend.app.api.routers.leads.async_session", sessionmaker)

    lead = Lead(title="AI chatbot for support", description="Need an AI chatbot using GPT for customer support")
    lead_ai = LeadAI(lead_id=lead.id, is_relevant=True, score=70)
    session.add(lead, lead_ai)
    await session.commit()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.patch(
            f"/api/leads/{lead.id}/status",
            json={"status": "saved"},
        )

    assert resp.status_code == 200
    assert resp.json()["status"] == "saved"
