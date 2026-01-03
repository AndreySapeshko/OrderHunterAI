import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker

from backend.app.api.main import app
from backend.app.db.session import get_session


@pytest.mark.asyncio
async def test_login_success(user, engine):
    sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False)

    async def override_get_session():
        async with sessionmaker() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=app)
    async with AsyncClient(base_url="http://test", transport=transport) as client:
        res = await client.post(
            "/api/auth/login",
            json={"email": user.email, "password": "password"},
        )

    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_login_wrong_password(user, engine):
    sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False)

    async def override_get_session():
        async with sessionmaker() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=app)
    async with AsyncClient(base_url="http://test", transport=transport) as client:
        res = await client.post(
            "/api/auth/login",
            json={"email": user.email, "password": "wrong"},
        )

    assert res.status_code == 401

    app.dependency_overrides.clear()
