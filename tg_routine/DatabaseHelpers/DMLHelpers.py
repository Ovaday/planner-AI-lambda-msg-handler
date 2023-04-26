from main import *

def insert_chat(connection, chat_id, update):
    username = ''
    if update:
        username = update.effective_chat.username

    cursor = connection.cursor()
    query = f"""INSERT INTO tg_bot_chat(chat_id, counter, is_approved, role, language, tokens_used, whisper_tokens,
                            last_conversation, username, current_mode, expenses) 
                            VALUES({chat_id}, 0, False, 'none', 'english', 0, 0, '', '{username}', 'chatGPT', 0);"""
    result = cursor.execute(query)
    connection.commit()
    cursor.close()
    return result

async def update_chat(connection, chat: Chat):
    cursor = connection.cursor()
    query = """
        UPDATE tg_bot_chat 
        SET 
            counter = %s,
            is_approved = %s,
            role = %s,
            language = %s,
            tokens_used = %s,
            whisper_tokens = %s,
            last_conversation = %s,
            username = %s,
            current_mode = %s,
            expenses = %s
        WHERE chat_id = %s;
    """
    values = (
        chat.counter,
        chat.is_approved,
        chat.role,
        chat.language,
        chat.tokens_used,
        chat.whisper_tokens,
        chat.last_conversation,
        chat.username,
        chat.current_mode,
        chat.expenses,
        chat.chat_id
    )
    result = cursor.execute(query, values)
    connection.commit()
    cursor.close()
    return result


async def tick_expenses(chat: Chat, tokens, model: str, is_classification=False):
    if "whisper" in model:
        chat.whisper_tokens += tokens
        print(type(chat.expenses))
        print(type(tokens))
        chat.expenses += 0.006 * tokens / 60


    if "ada" in model:
        if is_classification:
            chat.expenses += 0.0016 * tokens / 1000
        else:
            chat.expenses += 0.0004 * tokens / 1000
    elif "babbage" in model:
        if is_classification:
            chat.expenses += 0.0024 * tokens / 1000
        else:
            chat.expenses += 0.0005 * tokens / 1000
    elif "davinci" in model:
        chat.expenses += 0.02 * tokens / 1000
    else:
        chat.expenses += 0.002 * tokens / 1000
    await update_chat(db_connection, chat)

async_tick_expenses = async_to_sync(tick_expenses)
async_update_chat = async_to_sync(update_chat)