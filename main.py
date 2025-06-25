from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os
from wolframalpha import Client

# Environment variables (from Render secrets)
BOT_TOKEN = os.getenv("BOT_TOKEN")
WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID")

client = Client(WOLFRAM_APP_ID)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! I'm your 24/7 Math Bot. Just send me a math query!")

async def solve_math(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    try:
        res = client.query(query)
        answer = next(res.results).text
        await update.message.reply_text(f"✅ *{query}* = `{answer}`", parse_mode="Markdown")
    except Exception:
        await update.message.reply_text(f"❌ `{query}` → Sorry, I couldn't solve this.", parse_mode="Markdown")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), solve_math))
    print("✅ Bot is running...")
    app.run_polling()
