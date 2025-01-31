import typing

from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data
from aiogram.types.base import TelegramObject

from ..models.role import UserRole


class RoleFilter(BoundFilter):
    key = 'role'

    def __init__(
        self,
        role: typing.Union[None, UserRole, typing.Collection[UserRole]] = None,
    ):
        if role is None:
            self.roles = None
        elif isinstance(role, UserRole):
            self.roles = {role}
        else:
            self.roles = set(role)

    async def check(self, obj: TelegramObject):
        if self.roles is None:
            return True
        data = ctx_data.get()
        return data.get("role") in self.roles


class AdminFilter(BoundFilter):
    key = 'is_bot_admin'

    def __init__(self, is_bot_admin: typing.Optional[bool] = None):
        self.is_bot_admin = is_bot_admin

    async def check(self, obj: TelegramObject):
        if self.is_bot_admin is None:
            return True
        data = ctx_data.get()
        return (data.get("role") is UserRole.BOT_ADMIN) == self.is_bot_admin
