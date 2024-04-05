from config import DELAY_BETWEEN_NOTIFICATIONS_IN_SECONDS, DEFAULT_NOTIFICATION_TO_ADMIN, OWNERS_ID
import asyncio
from aiogram.types import Message
from aiogram import Bot
from models import Admin
from keyboards import get_show_notification_kb, get_notification_kb_for_admin
from database import admin_table, pet2admin_table
from models import Pet
from utils import make_pet_description

# NOTIFICATION_KEYBOARD = get_show_notification_kb()


async def _send_notification_to_admin(bot: Bot, admin_tg_id: Admin, pet: Pet, text: str, keyboard, greeting_text: str):
    try:
        await bot.send_photo(chat_id=admin_tg_id, photo=pet.pet_photo_id,
                    caption=text,
                    parse_mode="HTML",
                    reply_markup=keyboard)
        await bot.send_message(chat_id=admin_tg_id, text=greeting_text, parse_mode="HTML")
        await pet2admin_table.register_sent_msg(admin_tg_id, pet.uuid)
    except Exception as e:
        print(e)
    await asyncio.sleep(DELAY_BETWEEN_NOTIFICATIONS_IN_SECONDS)

async def _send_notification_to_owner(bot: Bot, owner_id: int, pet: Pet, text: str, greeting_text: str):
    try:
        await bot.send_photo(chat_id=owner_id, photo=pet.pet_photo_id,
                    caption=text,
                    parse_mode="HTML")
        await bot.send_message(chat_id=owner_id, text=greeting_text, parse_mode="HTML")
    except Exception as e:
        print(e)
    await asyncio.sleep(DELAY_BETWEEN_NOTIFICATIONS_IN_SECONDS)


async def send_pet_card_to_admins(bot: Bot, pet: Pet, city: str):
    admin_list = await admin_table.get_admins_for_notifications(city)
    print(f'len admin list = {admin_list}')
    if admin_list is None:
        print(f'NO ADMINS FOR {city}')
        return
    print('here')
    admin_list_ids = [admin.admin_tg_id for admin in admin_list]
    text = make_pet_description(pet)
    greeting_text = '<b>Появилась новая карточка питомца!</b>'
    keyboard = get_notification_kb_for_admin(pet_uuid=pet.uuid)
    
    # SEND TO ADMINS
    print(f'admin_list_ids = {admin_list_ids}')
    for owner_id in OWNERS_ID:
        print('HERE!!123')
        if owner_id not in admin_list_ids:
            print(f'SEND TO {owner_id}')
            await _send_notification_to_owner(bot, owner_id, pet, text, greeting_text)
            
    print('SENT TO ADMINs!!!')
    print(f'admin_list========={admin_list_ids}; {admin_list_ids is None}; {len(admin_list_ids)}')
    for admin_tg_id in admin_list_ids:
        print(f'SEND TO {admin_tg_id}')
        await _send_notification_to_admin(bot, admin_tg_id, pet, text, keyboard, greeting_text)

    