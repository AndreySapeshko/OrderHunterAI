import asyncio

from aiogram import Bot, Dispatcher

from backend.app.bot.handlers.actions import router as actions
from backend.app.config import TELEGRAM_BOT_TOKEN

dp = Dispatcher()
bot = Bot(TELEGRAM_BOT_TOKEN)
routers = [
    actions,
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
