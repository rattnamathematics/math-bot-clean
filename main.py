from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from sympy import symbols, Eq, solve, simplify
from sympy.parsing.sympy_parser import parse_expr
import re
import unicodedata

# 🔑 Insert your actual bot token below
BOT_TOKEN = "7598566406:AAGVb9k_K5TO40nUNy9pVD9a47pAUBgzCh0"

# 🔧 Clean and normalize input from users
def clean_input(text):
    text = unicodedata.normalize('NFKC', text)              # Fix hidden unicode
    text = text.lower()
    text = re.sub(r'\^', '**', text)                        # ^ → **
    text = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', text)        # 2x → 2*x
    text = re.sub(r'\s+', '', text)                         # remove all spaces
    return text

# 🎉 /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hi! I’m your Smart Math Bot 🤖\n\nTry sending:\n• solve 2x + 3 = 7\n• integrate x^2\n• factor x^2 + 5x + 6\n• differentiate sin(x)"
    )

# 💬 Main message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    raw_text = update.message.text
    text = clean_input(raw_text)

    print(f"📩 Raw input: {raw_text}")
    print(f"🧼 Cleaned input: {text}")

    x = symbols('x')

    try:
        if text.startswith("solve"):
            expr = text.replace("solve", "")
            if "=" not in expr:
                response = "❗ Please include '=' in your equation."
            else:
                left, right = expr.split("=")
                equation = Eq(parse_expr(left), parse_expr(right))
                solution = solve(equation, x)
                response = f"✅ Solution: x = {solution[0]}" if solution else "❌ No solution found."

        elif text.startswith("integrate"):
            expr = text.replace("integrate", "")
            result = parse_expr(expr).integrate()
            response = f"∫ Integral: {result}"

        elif text.startswith("differentiate") or text.startswith("derivative"):
            expr = text.replace("differentiate", "").replace("derivative", "")
            result = parse_expr(expr).diff()
            response = f"∂ Derivative: {result}"

        elif text.startswith("factor"):
            expr = text.replace("factor", "")
            result = simplify(parse_expr(expr)).factor()
            response = f"🧮 Factored: {result}"

        else:
            response = "🤖 Try one of these:\n• solve 2x + 3 = 7\n• integrate x^2\n• factor x^2 + 5x + 6\n• differentiate x^2"

    except Exception as e:
        print(f"⚠️ Exception: {e}")
        response = "❌ Error: Couldn’t solve this. Try something like: solve 2x + 3 = 7"

    await update.message.reply_text(response)

# 🛠️ Start the bot
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("🤖 Smart Math Bot is running...")
app.run_polling()
