# from typing import Any, Callable, Dict, Awaitable, Union
# from aiogram import BaseMiddleware
# from aiogram.types import TelegramObject


# class RegistrationMiddleware(BaseMiddleware):
#     def __init__(self, allowed_content_type: str):
#         # if isinstance(allowed_content_type, str):
#         #     allowed_content_type = [allowed_content_type]
#         self.allowed_content_type = allowed_content_type
#     async def __call__(
#             self,
#             handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
#             event: TelegramObject,
#             data: Dict[str, Any],
#     ) -> Any:
#         if self.allowed_content_type == 'button'
#         #user = data["event_from_user"]
#         #data["internal_id"] = self.get_internal_id(user.id)
#         return await handler(event, data)