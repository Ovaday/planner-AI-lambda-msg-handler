from asgiref.sync import sync_to_async
from ServiceHelpers import Chat


def __execute_query(cursor, query: str, single_record: bool):
    cursor.execute(query)
    cursor.execute(query)
    if single_record:
        return cursor.fetchone()
    else:
        return cursor.fetchall()


def __get_raw_chat(connection, chat_id: int):
    cursor = connection.cursor()
    query = f"select id, chat_id, counter, is_approved, role, language, tokens_used, last_conversation, username," \
            f" current_mode, expenses " \
            f"from tg_bot_chat " \
            f"where chat_id = '{chat_id}';"
    results= __execute_query(cursor, query, True)
    cursor.close()
    return Chat(*results)


def get_chat(connection, chat_id: int):
    chat = __get_raw_chat(connection, chat_id)
    # ToDO: resolve what to do when there is no chat
    return chat


def get_users_by_role(connection, role: str):
    cursor = connection.cursor()
    query = f"select id, chat_id, counter, is_approved, role, language, tokens_used, last_conversation, username," \
            f" current_mode, expenses " \
            f"from tg_bot_chat " \
            f"where role = '{role}';"
    results= __execute_query(cursor, query, False)
    cursor.close()
    chats = [Chat(*row) for row in results]
    return chats


def get_creator(connection):
    return __get_raw_chat(connection, 1)


async_get_chat = sync_to_async(get_chat)
async_get_creator = sync_to_async(get_creator)
async_get_users_by_role = sync_to_async(get_users_by_role)