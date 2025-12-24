import asyncio
import logging

from aiogram import Bot, Dispatcher

from backend.app.bot.handlers.actions import router as actions
from backend.app.config import TELEGRAM_BOT_TOKEN
from backend.app.bot.handlers.start import router as start

logger = logging.getLogger(__name__)

bot = Bot("8271265533:AAElBGmpX8YXNqFMr7ojNKA_kMCnNs1W3sI")
dp = Dispatcher()

routers = [
    actions,
    start,
]


def setup_routers(dp: Dispatcher, routers: list):
    for router in routers:
        dp.include_router(router)


async def main():

    setup_routers(dp, routers)
    print("🤖 Bot service started")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


def run():
    asyncio.run(main())


if __name__ == "__main__":
    run()
