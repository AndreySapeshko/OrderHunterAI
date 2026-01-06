from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.auth.dependencies import get_current_admin
from backend.app.api.schemas.admin import AdminUserOut
from backend.app.db.models.user import User
from backend.app.db.session import get_session

router = APIRouter()


@router.get("/users", response_model=list[AdminUserOut])
async def list_users(admin: User = Depends(get_current_admin), session: AsyncSession = Depends(get_session)):
    async with session:
        result = await session.execute(select(User).order_by(User.created_at.desc()))

    return result.scalars().all()


@router.get("/users/pending", response_model=list[AdminUserOut])
async def list_pending_users(admin: User = Depends(get_current_admin), session: AsyncSession = Depends(get_session)):
    async with session:
        result = await session.execute(select(User).where(User.is_active.is_(False)))

    return result.scalars().all()


@router.post("/users/{user_id}/activate")
async def activate_user(
    user_id: UUID, admin: User = Depends(get_current_admin), session: AsyncSession = Depends(get_session)
):
    async with session:
        user = await session.get(User, user_id)

        if not user:
            raise HTTPException(404, "User not found")

        user.is_active = True
        await session.commit()

    return {"status": "activated"}


@router.post("/users/{user_id}/deactivate")
async def deactivate_user(
    user_id: UUID, admin: User = Depends(get_current_admin), session: AsyncSession = Depends(get_session)
):
    async with session:
        user = await session.get(User, user_id)

        if not user:
            raise HTTPException(404, "User not found")

        user.is_active = False
        await session.commit()

    return {"status": "deactivated"}


@router.post("/users/{user_id}/make-admin")
async def make_admin(
    user_id: UUID, admin: User = Depends(get_current_admin), session: AsyncSession = Depends(get_session)
):
    async with session:
        user = await session.get(User, user_id)

        if not user:
            raise HTTPException(404, "User not found")

        user.is_admin = True
        await session.commit()

    return {"status": "admin_granted"}
