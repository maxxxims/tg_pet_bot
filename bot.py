from config import load_bot_token
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from handlers import commands, new_pet, find_pet
from db import init_db
import logging
logging.basicConfig(level=logging.INFO)


async def main():
    token = load_bot_token()
    print('RUN BOT!')
    print(f'token = {token}')
    bot = Bot(token=token, parse_mode='HTML')
    print('create bot')
    dp = Dispatcher()
    print('create dp')
    dp.include_routers(new_pet.router, find_pet.router, commands.router)
    print('create include routes')
    # await bot.delete_webhook(drop_pending_updates=True)
    await bot.delete_webhook()
    print('del webhoocks')
    await init_db()
    print(f'db init done!')
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())