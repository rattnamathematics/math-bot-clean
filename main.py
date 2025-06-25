import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
from wolframalpha import Client
from aiohttp import web

# ✅ Environment variables (from Render secrets)
BOT_TOKEN = os.getenv("BOT_TOKEN")
WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Example: https://yourapp.onrender.com/webhook

# ✅ Logging for debugging
logging.basicConfig(level=logging.INFO)

# ✅ Wolfram Alpha Client setup
client = Client(WOLFRAM_APP_ID)

# ✅ /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hi! I'm your math bot. Ask me any question!")

# ✅ /trick command for daily math trick
async def math_trick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    trick = (
        "✨ Quick Trick: To multiply any number by 11, just add the digits and place it in between.\n"
        "Example: 52 × 11 = 5(5+2)2 = 572"
    )
    await update.message.reply_text(trick)

# ✅ Handle all text queries (Wolfram Alpha)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    try:
        res = client.query(query)
        answer = next(res.results).text
        await update.message.reply_text(f"🧠 `{query}` → {answer}", parse_mode="Markdown")
    except Exception:
        await update.message.reply_text(f"❌ `{query}` → Sorry, I couldn't solve this.", parse_mode="Markdown")

# ✅ Webhook handler (matches the /webhook route)
async def handle_webhook(request):
    data = await request.json()
    await application.update_queue.put(Update.de_json(data, application.bot))
    return web.Response()

# ✅ Create the bot application and add handlers
application = ApplicationBuilder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("trick", math_trick))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# ✅ Aiohttp app for webhook routing (important: "/webhook" matches your WEBHOOK_URL)
app = web.Application()
app.router.add_post("/webhook", handle_webhook)

# ✅ Main function to run the webhook bot
async def run():
    await application.bot.set_webhook(url=WEBHOOK_URL)
    await application.initialize()
    await application.start()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()
    logging.info("🚀 Bot is live via webhook!")

# ✅ Start async loop
import asyncio
asyncio.run(run())
