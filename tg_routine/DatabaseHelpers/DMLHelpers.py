def insert_chat(connection, chat_id, update):
    username = ''
    if update:
        username = update.effective_chat.username

    cursor = connection.cursor()
    query = f"""INSERT INTO tg_bot_chat(chat_id, counter, is_approved, role, language, tokens_used, last_conversation, 
                            username, current_mode, expenses) 
                            VALUES({chat_id}, 0, False, 'none', 'english', 0, '', '{username}', 'chatGPT', 0);"""
    result = cursor.execute(query)
    connection.commit()
    cursor.close()
    return result
