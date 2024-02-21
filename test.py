from config import load_bot_token
import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters.command import Command
from aiogram.types import Message
# from handlers import commands, new_pet, find_pet
from db import init_db
import logging
import aiohttp
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardMarkup

logging.basicConfig(level=logging.INFO)


async def check_gpt_server():
    URL = 'http://162.248.227.166:4000/ping'
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            if response.status == 200:
                return True
            else:
                return False
            
router = Router()
@router.message()
async def pick_photo(message: Message):
    URL = 'http://162.248.227.166:4000/get_gpt_response'
    async with aiohttp.ClientSession() as session:
        json = {"prompt": message.text}
        async with session.post(URL, json=json) as response:
            json = await response.json()
            print(json.get('description'), json.get('status'))
            if int(json.get('status')) == 200:
                await message.answer(text=json.get('description'))
            else:
                await message.answer(text="Произошла ошибка. Попробуйте еще раз")
#     txt = """
#     строка 1
#     строка 2
#     \n \n строка три
# """ 
#     import emoji
#     txt2 = "строка 1 \nстрока 2"
#     txt3 = ":e-mail:Корпоративный аккаунт/почта/сервисы рассылок"
#     # txt4 = f"Корпоративный аккаунт/почта/сервисы рассылок c разрывом строки"
#     #{emoji.emojize(':e-mail:')} 
#     txt4 = f"Корпоративный аккаунт/почта/сервисы \nрассылок c разрывом строки"
#     kb = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [
#                 InlineKeyboardButton(text=txt2, callback_data='231'),
#             ], 
#             [InlineKeyboardButton(text=txt2, callback_data='3454')],
#         ])
#     await message.answer(text="test", reply_markup=kb)#, parse_mode='HTML')
#     ...
    


async def main():
    token = '6937977238:AAGZWXGSeheZy1eXfAJVC9mUvhl5fk7D358'
    bot = Bot(token=token, parse_mode='HTML')
    dp = Dispatcher()
    dp.include_routers(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    # import phonenumbers

    # my_string_number = "+7-913-517-26-86"
    # my_number = phonenumbers.parse(my_string_number)
    # print(phonenumbers.is_possible_number(my_number))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    asyncio.run(main())