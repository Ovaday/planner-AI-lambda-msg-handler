from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

from DatabaseHelpers import resolve_main_params
from main import db_connection
from translationHelpers import get_translation


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message, chat_id, chat = await resolve_main_params(db_connection, update)
    start_text = get_translation('start', chat.language)  # ToDO: add user chat resolve
    await context.bot.send_message(chat_id=chat_id, text=start_text)
    await context.bot.send_message(chat_id=chat_id, text=chat)
