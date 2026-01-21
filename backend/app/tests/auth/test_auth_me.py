import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker

from backend.app.api.main import app
from backend.app.db.session import get_session


@pytest.mark.asyncio
async def test_me_unauthorized(client, engine):
    sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False)

    async def override_get_session():
        async with sessionmaker() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    res = await client.get("/api/auth/me")
    assert res.status_code == 401

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_me_authorized(client, user, engine):
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

    res = await client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert res.status_code == 200
    data = res.json()
    assert data["email"] == user.email

    app.dependency_overrides.clear()
