from datetime import datetime

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker

from backend.app.api.main import app
from backend.app.db import Lead, LeadAI, RawItem, UserLead
from backend.app.db.session import get_session


@pytest.mark.asyncio
async def test_get_leads(user, engine):
    sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False)

    async def override_get_session():
        async with sessionmaker() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=app)
    async with AsyncClient(base_url="http://test", transport=transport) as client:
        login = await client.post(
            "/api/auth/login",
            json={"email": user.email, "password": "password"},
        )
        token = login.json()["access_token"]
        resp = await client.get(
            "/api/leads/",
            headers={"Authorization": f"Bearer {token}"},
        )

    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_user_leads(engine, user):
    sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False)

    async def override_get_session():
        async with sessionmaker() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=app)
    async with AsyncClient(base_url="http://test", transport=transport) as client:
        login = await client.post(
            "/api/auth/login",
            json={"email": user.email, "password": "password"},
        )
        token = login.json()["access_token"]

        resp = await client.get(
            "/api/user_leads/",
            headers={"Authorization": f"Bearer {token}"},
        )

    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_raw_items(engine, user):
    sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False)

    async def override_get_session():
        async with sessionmaker() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    transport = ASGITransport(app=app)
    async with AsyncClient(base_url="http://test", transport=transport) as client:
        login = await client.post(
            "/api/auth/login",
            json={"email": user.email, "password": "password"},
        )
        token = login.json()["access_token"]
        resp = await client.get(
            "/api/raw_items/",
            headers={"Authorization": f"Bearer {token}"},
        )

    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_lead_by_id(session, user, engine):
    sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False)

    async def override_get_session():
        async with sessionmaker() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
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
        login = await client.post(
            "/api/auth/login",
            json={"email": user.email, "password": "password"},
        )
        token = login.json()["access_token"]
        resp = await client.get(
            f"/api/leads/{lead.id}",
            headers={"Authorization": f"Bearer {token}"},
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == str(lead.id)

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_user_lead_by_id(session, user, engine):
    sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False)

    async def override_get_session():
        async with sessionmaker() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
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
    user_lead = UserLead(lead_id=lead.id, user_id=user.id)
    session.add(user_lead)
    await session.commit()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        login = await client.post(
            "/api/auth/login",
            json={"email": user.email, "password": "password"},
        )
        token = login.json()["access_token"]
        resp = await client.get(
            f"/api/user_leads/{user_lead.id}",
            headers={"Authorization": f"Bearer {token}"},
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == str(user_lead.id)

    app.dependency_overrides.clear()


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
