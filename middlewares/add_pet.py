from typing import Any, Callable, Dict, Awaitable, Union
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from database import pet_table

class AddingPetMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        state = data['state']
        data['uuid'] = (await state.get_data())['uuid']
        print('CALLBACK MIDLEWARE \n')
        await event.message.delete()
        #try:    await event.message.delete()
        #except:  ...
        # print('\n')
        # print(f'msg text = {event.message.text}')
        # print(f'{data["event_update"].message}')
        #if event.message.text != '/exit':
        sent_msg =  await handler(event, data)
        if sent_msg is not None:
           print('******************** ADDED SENT_MSG')
           print(f'msg id = {sent_msg.message_id}; chat_id = {sent_msg.chat.id}')
           await state.update_data(sent_msg_id=sent_msg.message_id)
        else:
            await state.update_data(sent_msg_id=None)
        #print(f'sent msg = {sent_msg}; {type(sent_msg)}')
        return sent_msg
    

class AddingPetSkipTextMiddleware(BaseMiddleware):
    def __init__(self, allowed_text_states: list) -> None:
        self.allowed_text_states = allowed_text_states


    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        # try:    await event.delete()
        # except Exception as e:  print(e)
        #print(data['event_chat']) #event_update
        print(f'MESSAGE MIDDLEWARE! \n')
        state = data['state']
        current_state = await state.get_state()

        uuid = (await state.get_data())['uuid']
        data['uuid'] = uuid

        state_data = await state.get_data()
        if state_data.get('sent_msg_id', None) is not None:
            print('********************')
            print(f'msg id = {event.chat.id}; chat_id = {state_data.get("sent_msg_id")}')
            await data['bot'].delete_message(chat_id=event.chat.id,
                                        message_id=state_data.get('sent_msg_id'))
            await state.update_data(sent_msg_id=None)
        # else:
        #     await state.update_data(sent_msg_id=None)
        # print(f'{data.keys()}')
        #print(f'SENT MSG ID = {state_data.get("sent_msg_id", None)}')

        user_text = data["event_update"].message.text
        if user_text is not None:
            if user_text == '/exit':
                await pet_table.delete_pet(uuid)
                await state.set_state(None)
                await event.answer(text='Регистрация карточки питомца завершена')
                return 
            elif current_state in self.allowed_text_states:
                #print('YEEEEESS!')
                sent_msg = await handler(event, data)
                if sent_msg is not None:
                    await state.update_data(sent_msg_id=sent_msg.message_id)
                else:
                    await state.update_data(sent_msg_id=None)
                return sent_msg
            else:
                await event.answer(text='Чтобы оставновить регистрацию карточки питомца введите /exit')
                return 
        return await handler(event, data)