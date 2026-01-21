from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.auth.dependencies import get_current_user
from backend.app.api.auth.jwt import create_access_token
from backend.app.api.auth.security import hash_password, verify_password
from backend.app.api.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserOut
from backend.app.db.models.user import User
from backend.app.db.session import get_session

router = APIRouter()


@router.post("/register")
async def register(data: RegisterRequest, session: AsyncSession = Depends(get_session)):
    async with session:
        exists = await session.scalar(select(User).where(User.email == data.email))
        if exists:
            raise HTTPException(400, "Email already registered")

        user = User(
            email=data.email,
            password_hash=hash_password(data.password),
            is_active=False,
            is_admin=False,
        )
        session.add(user)
        await session.commit()

    return {"message": "Registration submitted for approval"}


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, session: AsyncSession = Depends(get_session)):
    async with session:
        user = await session.scalar(select(User).where(User.email == data.email))

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")

    if not user.is_active:
        raise HTTPException(403, "Account not approved yet")

    token = create_access_token(subject=str(user.id))

    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserOut)
async def me(current_user=Depends(get_current_user)):
    return current_user
