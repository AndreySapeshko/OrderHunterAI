from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from backend.app.db.crud import get_user_by_email
from backend.app.db.session import async_session

router = Router()


@router.message(Command("link"))
async def link_bot(message: Message, command: CommandObject):
    print("ENTER link_bot")
    if not command.args:
        await message.answer("Укажите свой email в таком \n" "формате: /link example@example.com")
        return
    email = command.args.strip()
    telegram_id = message.from_user.id
    username = message.from_user.username

    async with async_session() as session:
        user = await get_user_by_email(email, session)
        if not user:
            return await message.answer("Сначала пройдите регистрацию на сайте: https://my_site.com")

        if not user.is_active:
            return await message.answer(
                "Ваша регистрация еще не активирована.\n" " Дождитесь активации и попробуйте снова."
            )

        if user.chat_id:
            return await message.answer("Ваш telegram уже подключен.")

        user.chat_id = telegram_id
        user.username = username
        await session.commit()
        return await message.answer(
            f"Ты успешно подключен.\n"
            f"Твой ID: {user.chat_id}\n"
            f"Имя: {user.username}\n"
            "OrderHunterAI запущен. 🚀\n"
            "Теперь ты будешь получать уведомления о заказах."
        )
