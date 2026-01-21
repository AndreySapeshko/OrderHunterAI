import asyncio
from getpass import getpass

from sqlalchemy import select

from backend.app.api.auth.security import hash_password
from backend.app.db import User
from backend.app.db.session import async_session


async def create_admin():
    email = input("Admin email: ").strip()

    if not email:
        print("Email is required")
        return

    password_1 = getpass("Password: ")

    if password_1.lower() == "exit":
        print("Cancelled")
        return

    password_2 = getpass("Repeat password: ")

    if password_1 != password_2:
        print("Passwords do not match")
        return

    async with async_session() as session:

        existing = await session.scalar(select(User).where(User.email == email))

        if existing:
            print("User with this email already exists")
            return

        user = User(
            email=email,
            password_hash=hash_password(password_1),
            is_active=True,
            is_admin=True,
        )

        session.add(user)
        await session.commit()

    print(f"Admin user created: {email}")


if __name__ == "__main__":
    asyncio.run(create_admin())
