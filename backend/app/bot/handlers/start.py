from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("start"))
async def start_cmd(message: Message):
    print(f"ENTER start_cmd telegram_id: {message.from_user.id}")

    await message.answer(
        "👋 Привет!\n\n"
        "Я могу отправлять уведомления\n"
        "о новых отобранных заказах. 🚀\n"
        "Что бы получать уведомления,\n"
        "сначала пройдите регистрацию\n"
        "на сайте: https://my_site.com, затем\n"
        "email указанный при регистрации отправьте\n"
        "мне в формате: /link example@example.com"
    )
