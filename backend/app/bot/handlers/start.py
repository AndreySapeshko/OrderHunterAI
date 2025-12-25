from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from backend.app.db.crud import get_or_create_user
from backend.app.db.session import async_session

router = Router()


@router.message(Command("start"))
async def start_cmd(message: Message):
    print(f"ENTER start_cmd telegram_id: {message.from_user.id}")
    telegram_id = message.from_user.id
    username = message.from_user.username

    async with async_session() as session:
        user = await get_or_create_user(
            session=session,
            telegram_id=telegram_id,
            username=username,
        )
        await session.commit()

    await message.answer(
        f"👋 Привет!\n\n"
        f"Ты успешно зарегистрирован.\n"
        f"Твой ID: {user.chat_id}\n"
        f"Имя: {user.username}\n"
        "OrderHunterAI запущен. 🚀\n"
        "Теперь ты будешь получать уведомления о заказах."
    )
