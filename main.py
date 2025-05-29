import asyncio
import aiohttp
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

BOT_TOKEN = "7715758090:AAG0zZh85o9jpmmtMgmRvi2oqpC8IWXo6hk"
CHAT_ID = 7883022926

target_url = None
requests_per_second = 0
running = False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="👋 Merhaba! Lütfen hedef URL'yi gönderin.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global target_url, requests_per_second, running

    msg = update.message.text.strip()

    if target_url is None:
        target_url = msg
        await context.bot.send_message(chat_id=update.effective_chat.id, text="📥 Hedef URL kaydedildi.
Kaç istek/saniye yapılacağını yazın:")
        return

    if requests_per_second == 0:
        try:
            requests_per_second = int(msg)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"🚀 Başlatılıyor: {requests_per_second} req/s → {target_url}")
            asyncio.create_task(send_requests(context.bot))
        except ValueError:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="❌ Geçerli bir sayı girin.")
        return

async def send_requests(bot):
    global target_url, requests_per_second, running
    running = True
    interval = 1 / requests_per_second
    count = 0
    async with aiohttp.ClientSession() as session:
        while running:
            try:
                async with session.get(target_url) as response:
                    print(f"[{count}] Status: {response.status}")
            except Exception as e:
                print(f"[{count}] HATA: {e}")
                await bot.send_message(chat_id=CHAT_ID, text=f"❗ Hata: {e}")
            count += 1
            await asyncio.sleep(interval)

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
