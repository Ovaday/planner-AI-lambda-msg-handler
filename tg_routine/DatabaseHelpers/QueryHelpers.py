from typing import Optional

from main import *
from .DBModels import all_fields
from .DMLHelpers import insert_chat


def __execute_query(cursor, query: str, single_record: bool):
    cursor.execute(query)
    if single_record:
        return cursor.fetchone()
    else:
        return cursor.fetchall()


def __get_raw_chat(connection, chat_id: int) -> Optional[Chat]:
    cursor = connection.cursor()
    query = f"select {all_fields} " \
            f"from tg_bot_chat " \
            f"where chat_id = '{chat_id}';"
    results = __execute_query(cursor, query, True)
    cursor.close()
    if not results:
        return None
    return Chat(*results)


def get_chat(connection, chat_id: int, update):
    chat = __get_raw_chat(connection, chat_id)
    print('get chat')
    print(chat)
    if not chat:
        print('not chat')
        insert_chat(connection, chat_id, update)
        chat = __get_raw_chat(connection, chat_id)
    return chat


def get_users_by_role(connection, role: str):
    cursor = connection.cursor()
    query = f"select {all_fields} " \
            f"from tg_bot_chat " \
            f"where role = '{role}';"
    results= __execute_query(cursor, query, False)
    cursor.close()
    if not results or len(results) == 0:
        return []
    chats = [Chat(*row) for row in results]
    return chats


def get_creator(connection):
    return __get_raw_chat(connection, 1)


async_get_chat = sync_to_async(get_chat)
async_get_creator = sync_to_async(get_creator)
async_get_users_by_role = sync_to_async(get_users_by_role)