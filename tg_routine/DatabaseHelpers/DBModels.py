from collections import namedtuple

Chat = namedtuple('Chat', ['id', 'chat_id', 'counter', 'is_approved', 'role', 'language', 'tokens_used',
                           'last_conversation', 'username', 'current_mode', 'expenses'])
