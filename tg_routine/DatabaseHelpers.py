import psycopg2
from asgiref.sync import sync_to_async
from telegram import Update

from main import secrets


def set_db_connection():
    DB_USER = secrets['DB_USER']
    DB_PASSWORD = secrets['DB_PASSWORD']
    DB_HOST = secrets['DB_HOST']
    DB_NAME = secrets['DB_NAME']

    connection = psycopg2.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST,
                                  database=DB_NAME)
    return connection


def get_chat(connection, chat_id: int):
    cursor = connection.cursor()
    query = f"select * from tg_bot_chat where chat_id = {chat_id};"
    cursor.execute(query)
    results = cursor.fetchone()
    # ToDO: resolve what to do when there is no chat
    cursor.close()
    return results


async def resolve_main_params(update: Update):
    message = update.message
    chat_id = update.effective_chat.id

    chat = await async_get_chat(chat_id)
    return message, chat_id, chat


async_get_chat = sync_to_async(get_chat)