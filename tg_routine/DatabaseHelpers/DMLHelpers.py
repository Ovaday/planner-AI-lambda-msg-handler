"""class Chat(models.Model):
    chat_id = models.CharField(max_length=300)
    counter = models.IntegerField(default=0)
    tokens_used = models.IntegerField(default=0)
    expenses = models.FloatField(default=0)

    is_approved = models.BooleanField(default=False)
    role = models.CharField(choices=[('admin', 'admin'),
                                     ('parents', 'parents'),
                                     ('user', 'user'),
                                     ('none', 'none'), ],
                            default='none',
                            max_length=10)
    language = models.CharField(choices=[('russian', 'russian'),
                                         ('english', 'english'), ],
                                default='english',
                                max_length=10)
    last_conversation = models.TextField(default='', null=True, blank=True)
    username = models.CharField(max_length=300, default='', null=True, blank=True)
    current_mode = models.CharField(max_length=300, default='chatGPT')"""


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
