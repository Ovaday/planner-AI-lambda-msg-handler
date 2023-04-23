from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

from translationHelpers import get_translation


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_text = get_translation('start', 'english')  # ToDO: add user chat resolve
    await context.bot.send_message(chat_id=update.effective_chat.id, text=start_text)
