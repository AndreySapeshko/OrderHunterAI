import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker

from backend.app.api.main import app
from backend.app.db.session import get_session


@pytest.mark.asyncio
async def test_admin_approve_user(client, admin, user_not_active, engine):
    sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False)

    async def override_get_session():
        async with sessionmaker() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    login = await client.post(
        "/api/auth/login",
        json={"email": admin.email, "password": "adminpass"},
    )
    token = login.json()["access_token"]

    res = await client.post(
        f"/api/admin/users/{user_not_active.id}/activate",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert res.status_code == 200

    app.dependency_overrides.clear()
