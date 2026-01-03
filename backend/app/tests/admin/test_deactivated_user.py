import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker

from backend.app.api.main import app
from backend.app.db.session import get_session


@pytest.mark.asyncio
async def test_deactivated_user_cannot_login(client, engine, user_not_active):
    sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False)

    async def override_get_session():
        async with sessionmaker() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    res = await client.post(
        "/api/auth/login",
        json={"email": user_not_active.email, "password": "password"},
    )

    assert res.status_code == 401

    app.dependency_overrides.clear()
