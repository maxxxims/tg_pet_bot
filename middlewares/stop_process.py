from typing import Any, Callable, Dict, Awaitable, Union
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from database import pet_table


    

class StopProcessMiddleware(BaseMiddleware):
    def __init__(self, exit_action: callable) -> None:
        self.exit_action = exit_action


    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        user_text = data["event_update"].message.text
        state = data['state']
        print(f'MIDLEWARE TEXT  + {user_text}')
        if user_text is not None:
            if '/exit' in user_text:
                await state.set_state(None)
                await self.exit_action(event, state, data)
                return 
            else:
                sent_msg = await handler(event, data)
                return sent_msg
            
        return await handler(event, data)