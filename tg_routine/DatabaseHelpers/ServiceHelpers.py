from telegram import Update
from .QueryHelpers import async_get_chat


async def resolve_main_params(db_connection, update: Update):
    message = update.message
    chat_id = update.effective_chat.id

    chat = await async_get_chat(db_connection, chat_id, update)
    return message, chat_id, chat



