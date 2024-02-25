from typing import Any, Callable, Dict, Awaitable, Union
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from database import volunteer_table


class AddUserNameMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        user = data["event_from_user"]
        is_voulnteer = await volunteer_table.is_volounteer(user.id)
        if is_voulnteer:
            await volunteer_table.update_column(user.id, username=user.username)
        print(f'USER ID = {user.id}; username = {user.username}; {user.full_name}')
        return await handler(event, data)