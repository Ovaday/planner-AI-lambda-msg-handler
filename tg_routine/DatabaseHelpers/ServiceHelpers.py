import psycopg2
from telegram import Update
from collections import namedtuple

from .QueryHelpers import async_get_chat
from ..main import secrets


def set_db_connection():
    DB_USER = secrets['DB_USER']
    DB_PASSWORD = secrets['DB_PASSWORD']
    DB_HOST = secrets['DB_HOST']
    DB_NAME = secrets['DB_NAME']

    connection = psycopg2.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST,
                                  database=DB_NAME)
    return connection


Chat = namedtuple('Chat', ['id', 'chat_id', 'counter', 'is_approved', 'role', 'language', 'tokens_used',
                           'last_conversation', 'username', 'current_mode', 'expenses'])


async def resolve_main_params(db_connection, update: Update):
    message = update.message
    chat_id = update.effective_chat.id

    chat = await async_get_chat(db_connection, chat_id)
    return message, chat_id, chat



