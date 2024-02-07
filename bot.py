from config import load_bot_token
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from handlers import commands, new_pet, find_pet
from db import init_db


async def main():
    token = load_bot_token()
    print('RUN BOT!')
    bot = Bot(token=token, parse_mode='HTML')
    dp = Dispatcher()
    dp.include_routers(new_pet.router, find_pet.router, commands.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())