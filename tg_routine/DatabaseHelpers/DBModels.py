from typing import Optional

from main import db_connection
from dataclasses import dataclass

all_fields = "id, chat_id, counter, is_approved, role, language, tokens_used, whisper_tokens," \
             "last_conversation, username, current_mode, expenses"

@dataclass
class Chat:
    id: int
    chat_id: int
    counter: int# = 0
    tokens_used: int# = 0
    whisper_tokens: float# = 0.0
    expenses: float# = 0.0
    is_approved: bool# = False
    role: str# = 'none'
    language: str# = 'english'
    last_conversation: str# = ''
    username: str# = ''
    current_mode: str# = 'chatGPT'

    def __init__(
        self,
        id: int,
        chat_id: int,
        counter: Optional[int] = 0,
        is_approved: Optional[bool] = False,
        role: Optional[str] = 'none',
        language: Optional[str] = 'english',
        tokens_used: Optional[int] = 0,
        whisper_tokens: Optional[float] = 0.0,
        last_conversation: Optional[str] = '',
        username: Optional[str] = '',
        current_mode: Optional[str] = 'chatGPT',
        expenses: Optional[float] = 0.0
    ):
        self.id = id
        self.chat_id = chat_id
        self.counter = int(counter)
        self.tokens_used = int(tokens_used)
        self.whisper_tokens = float(whisper_tokens)
        self.expenses = float(expenses)
        self.is_approved = bool(is_approved)
        self.role = str(role)
        self.language = str(language)
        self.last_conversation = str(last_conversation)
        self.username = str(username)
        self.current_mode = str(current_mode)

    def money_used(self) -> str:
        return f'$ {self.expenses}'

    async def save(self):
        from DMLHelpers import update_chat
        await update_chat(db_connection, self)

