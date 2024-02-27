from config import load_bot_token
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from handlers import commands, new_pet, find_pet, volunteer_registration, \
admin_registration, notifications, manage_pets
from db import init_db, drop_db
import logging
import aiohttp


logging.basicConfig(level=logging.INFO)


async def check_gpt_server():
    URL = 'http://162.248.227.166:4000/ping'
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            if response.status == 200:
                return True
            else:
                return False
            

def get_bot_commands():
    bot_commands = [
        types.BotCommand(command="/registration", description="Регистрация"),
        types.BotCommand(command="/pets", description="Посмотреть карточки питомцев"),
        types.BotCommand(command="/new", description="Добавить питомца"),
        types.BotCommand(command="/statistics", description="Статистика"),
    ]
    return bot_commands


async def main():
    token = load_bot_token()
    # print(f'token = {token}')
    print('RUN BOT!')
    bot = Bot(token=token, parse_mode='HTML')
    dp = Dispatcher()
    dp.include_routers(
        new_pet.router, #find_pet.router,
        commands.router,
        volunteer_registration.router, admin_registration.router,
        notifications.router, manage_pets.router
        )
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=get_bot_commands())
    # await drop_db()
    await init_db()
    connection_to_gpt = await check_gpt_server()
    print(f'connection_to_gpt = {connection_to_gpt}')

    

    await dp.start_polling(bot)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    # asyncio.run(main())