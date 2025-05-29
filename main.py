import asyncio
import aiohttp
from telegram import Bot
import os

# Ortam değişkenlerinden çek (Railway'e özel)
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))
TARGET_URL = os.getenv("TARGET_URL", "https://webhook.site/8d491bca-da81-4c68-ab42-eb19d8ef6607")
REQUESTS_PER_SECOND = int(os.getenv("REQUESTS_PER_SECOND", 50))
INTERVAL = 1 / REQUESTS_PER_SECOND

bot = Bot(token=BOT_TOKEN)

async def send_request(session, count):
    try:
        async with session.get(TARGET_URL) as response:
            status = response.status
            print(f"[{count}] Status: {status}")
    except Exception as e:
        print(f"[{count}] Hata: {e}")
        await bot.send_message(chat_id=CHAT_ID, text=f"🚨 Hata oluştu: {str(e)}")

async def main():
    await bot.send_message(chat_id=CHAT_ID, text="🚀 Railway bot başlatıldı.")
    count = 0
    async with aiohttp.ClientSession() as session:
        while True:
            asyncio.create_task(send_request(session, count))
            count += 1
            await asyncio.sleep(INTERVAL)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Durdu.")
