from enum import Enum


class UserRole(Enum):
    BOT_ADMIN = "bot_admin"
    CHAT_ADMIN = "chat_admin"
    USER = "user"
