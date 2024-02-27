from config import DELAY_BETWEEN_NOTIFICATIONS_IN_SECONDS, DEFAULT_NOTIFICATION_TO_ADMIN
import asyncio
from aiogram.types import Message
from aiogram import Bot
from models import Admin
from keyboards import get_show_notification_kb, get_notification_kb_for_admin
from database import admin_table, pet2admin_table
from models import Pet
from utils import make_pet_description

# NOTIFICATION_KEYBOARD = get_show_notification_kb()


async def test(message: Message):
    for i in range(5):
        await message.answer(text=f'HELLOW IT IS {i} iteration!')
        await asyncio.sleep(5)


async def send_notification_to_admins(bot: Bot, admin_list: list = None, kb = None):
    #kb = get_show_notification_kb()
    for admn in admin_list:
        try:
            await bot.send_message(chat_id=admn.admin_tg_id,
                            text=DEFAULT_NOTIFICATION_TO_ADMIN,
                            reply_markup=kb)
        except Exception as e:
            print(e)

        await asyncio.sleep(DELAY_BETWEEN_NOTIFICATIONS_IN_SECONDS)
    


async def send_notification_in_one_city(bot: Bot, city: str):
    admin_list = await admin_table.get_admins_for_notifications(city)
    if admin_list is None:
        return
    kb = get_show_notification_kb(city=city)
    await send_notification_to_admins(bot, admin_list, kb)



async def send_pet_card_to_admins(bot: Bot, pet: Pet, city: str):
    admin_list = await admin_table.get_admins_for_notifications(city)
    if admin_list is None:
        return
    text = '<u><b>Появилась новая карточка питомца!</b></u> \n' + make_pet_description(pet)
    keyboard = get_notification_kb_for_admin(pet_uuid=pet.uuid)
    for admn in admin_list:
        try:
            await bot.send_photo(chat_id=admn.admin_tg_id, photo=pet.pet_photo_id,
                        caption=text,
                        parse_mode="HTML",
                        reply_markup=keyboard)
            await pet2admin_table.register_sent_msg(admn.admin_tg_id, pet.uuid)
        except Exception as e:
            print(e)
        await asyncio.sleep(DELAY_BETWEEN_NOTIFICATIONS_IN_SECONDS)

