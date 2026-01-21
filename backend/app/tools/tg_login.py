import asyncio
import os

from telethon import TelegramClient

API_ID = int(os.environ["TELEGRAM_API_ID"])
API_HASH = os.environ["TELEGRAM_API_HASH"]

# Важно: это имя файла сессии. Получится tg_session.session
SESSION_NAME = os.environ.get("TELETHON_SESSION", "tg_session")


async def main():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.start()  # попросит телефон/код/2FA (если включено)
    me = await client.get_me()
    print(f"✅ Logged in as: {me.username or me.first_name} (id={me.id})")
    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
