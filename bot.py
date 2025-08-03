# bot.py

from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from telegram import Update
from ai_core import generate_workout

import os
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Приветствие
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 Привет! Я GymGPT — бот, который составляет тренировки с помощью GPT.\n\n"
        "📌 Что я умею:\n"
        "• Составляю тренировки по твоему запросу (русский / английский)\n"
        "• Умею переводить последнюю тренировку на английский, если попросишь\n\n"
        "💬 Примеры запросов:\n"
        "• Тренировка на спину\n"
        "• Хочу упражнения для пресса\n"
        "• Workout for legs\n"
        "• Переведи на английский\n\n"
        "Напиши, что хочешь прокачать — и я предложу программу 💪"
    )
    await update.message.reply_text(text)

# Основная логика
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    await update.message.reply_text("💬 Got it! Generating your workout...")

    last_workout = context.user_data.get("last_workout", "")
    result = await generate_workout(user_input, last_workout)

    if "подхода" in result or "повторений" in result or "workout" in result.lower():
        context.user_data["last_workout"] = result

    await update.message.reply_text(result)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Bot is running...")
    app.run_polling()
