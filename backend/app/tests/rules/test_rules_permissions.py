import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker

from backend.app.api.main import app
from backend.app.db.session import get_session


@pytest.mark.asyncio
async def test_cannot_see_other_user_rules(client: AsyncClient, user, other_user, engine):
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

    # rule от первого пользователя
    await client.post(
        "/api/user_rules/", json={"include_keywords": ["private"]}, headers={"Authorization": f"Bearer {token}"}
    )

    # второй пользователь смотрит список
    login_2 = await client.post(
        "/api/auth/login",
        json={"email": other_user.email, "password": "user_2pass"},
    )
    token_2 = login_2.json()["access_token"]
    r = await client.get("/api/user_rules/", headers={"Authorization": f"Bearer {token_2}"})

    assert r.status_code == 200
    rules = r.json()

    assert all("private" not in (rule.get("include_keywords") or []) for rule in rules)

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_cannot_update_other_users_rule(client: AsyncClient, user, other_user, engine):
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
        "/api/user_rules/", json={"include_keywords": ["secret"]}, headers={"Authorization": f"Bearer {token}"}
    )

    rule_id = create.json()["id"]

    login_2 = await client.post(
        "/api/auth/login",
        json={"email": other_user.email, "password": "user_2pass"},
    )
    token_2 = login_2.json()["access_token"]

    r = await client.patch(
        f"/api/user_rules/{rule_id}", json={"enabled": False}, headers={"Authorization": f"Bearer {token_2}"}
    )

    assert r.status_code == 404

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_cannot_delete_other_users_rule(client: AsyncClient, user, other_user, engine):
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
        "/api/user_rules/", json={"include_keywords": ["nope"]}, headers={"Authorization": f"Bearer {token}"}
    )

    rule_id = create.json()["id"]

    login_2 = await client.post(
        "/api/auth/login",
        json={"email": other_user.email, "password": "user_2pass"},
    )
    token_2 = login_2.json()["access_token"]

    r = await client.delete(f"/api/user_rules/{rule_id}", headers={"Authorization": f"Bearer {token_2}"})

    assert r.status_code == 404

    app.dependency_overrides.clear()
