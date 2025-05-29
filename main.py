import asyncio
import aiohttp
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

BOT_TOKEN = "7715758090:AAG0zZh85o9jpmmtMgmRvi2oqpC8IWXo6hk"
CHAT_ID = 7883022926

target_url = None
total_requests = 0
concurrent_threads = 0

stage = "url"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global stage, target_url, total_requests, concurrent_threads
    stage = "url"
    target_url = None
    total_requests = 0
    concurrent_threads = 0
    await context.bot.send_message(chat_id=update.effective_chat.id, text="👋 Hedef URL'yi gönderin:")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global stage, target_url, total_requests, concurrent_threads

    msg = update.message.text.strip()

    if stage == "url":
        target_url = msg
        stage = "count"
        await context.bot.send_message(chat_id=update.effective_chat.id, text="🔢 Kaç istek gönderilsin (toplam)?:")
        return

    if stage == "count":
        try:
            total_requests = int(msg)
            stage = "threads"
            await context.bot.send_message(chat_id=update.effective_chat.id, text="🧵 Kaç eşzamanlı thread (görev) kullanılsın?:")
        except ValueError:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="❌ Geçerli bir sayı gir.")
        return

    if stage == "threads":
        try:
            concurrent_threads = int(msg)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"🚀 Başlatılıyor:
URL: {target_url}
Toplam istek: {total_requests}
Thread sayısı: {concurrent_threads}")
            await run_requests(context.bot)
            stage = "url"
        except ValueError:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="❌ Geçerli bir sayı gir.")
        return

async def send_single_request(session, count):
    try:
        async with session.get(target_url) as response:
            print(f"[{count}] Status: {response.status}")
    except Exception as e:
        print(f"[{count}] HATA: {e}")
        await Bot(BOT_TOKEN).send_message(chat_id=CHAT_ID, text=f"❗ Hata: {e}")

async def run_requests(bot):
    sem = asyncio.Semaphore(concurrent_threads)
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(total_requests):
            async def bounded_request(i=i):
                async with sem:
                    await send_single_request(session, i)
            tasks.append(asyncio.create_task(bounded_request()))
        await asyncio.gather(*tasks)
    await bot.send_message(chat_id=CHAT_ID, text="✅ Tüm istekler gönderildi.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
