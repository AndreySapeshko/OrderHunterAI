import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker

from backend.app.api.main import app
from backend.app.db.session import get_session


@pytest.mark.asyncio
async def test_create_rule(client: AsyncClient, user, engine):
    sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False)

    async def override_get_session():
        async with sessionmaker() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    payload = {
        "source_id": ["telegram"],
        "include_keywords": ["python", "bot"],
        "exclude_keywords": ["resume"],
        "min_text_length": 200,
        "min_score": 2,
        "enabled": True,
    }

    login = await client.post(
        "/api/auth/login",
        json={"email": user.email, "password": "password"},
    )
    token = login.json()["access_token"]

    r = await client.post(
        "/api/user_rules/",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert r.status_code == 200
    data = r.json()

    assert data["source_id"] == ["telegram"]
    assert "id" in data
    assert data["enabled"] is True

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_list_rules(client: AsyncClient, user, engine):
    sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False)

    async def override_get_session():
        async with sessionmaker() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    login = await client.post(
        "/api/auth/login",
        json={"email": user.email, "password": "password"},
    )
    token = login.json()["access_token"]

    r = await client.get(
        "/api/user_rules/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert r.status_code == 200
    assert isinstance(r.json(), list)

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_update_rule(client: AsyncClient, user, engine):
    sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False)

    async def override_get_session():
        async with sessionmaker() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    login = await client.post(
        "/api/auth/login",
        json={"email": user.email, "password": "password"},
    )
    token = login.json()["access_token"]

    create = await client.post(
        "/api/user_rules/",
        json={"include_keywords": ["ai"]},
        headers={"Authorization": f"Bearer {token}"},
    )

    rule_id = create.json()["id"]

    r = await client.patch(
        f"/api/user_rules/{rule_id}",
        json={"enabled": False, "min_score": 5},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert r.status_code == 200
    data = r.json()
    assert data["enabled"] is False
    assert data["min_score"] == 5

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_delete_rule(client: AsyncClient, user, engine):
    sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False)

    async def override_get_session():
        async with sessionmaker() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    login = await client.post(
        "/api/auth/login",
        json={"email": user.email, "password": "password"},
    )
    token = login.json()["access_token"]

    create = await client.post(
        "/api/user_rules/",
        json={"include_keywords": ["delete_me"]},
        headers={"Authorization": f"Bearer {token}"},
    )

    rule_id = create.json()["id"]

    r = await client.delete(
        f"/api/user_rules/{rule_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert r.status_code == 200

    # Проверяем, что правило реально удалено
    r2 = await client.get(
        "/api/user_rules/",
        headers={"Authorization": f"Bearer {token}"},
    )

    ids = [x["id"] for x in r2.json()]
    assert rule_id not in ids

    app.dependency_overrides.clear()
