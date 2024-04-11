from config import DELAY_BETWEEN_NOTIFICATIONS_IN_SECONDS, OWNERS_ID
import asyncio
from aiogram.types import Message
from aiogram import Bot, html
from models import Admin
from models import Volunteer, Admin


async def _get_user_info(bot: Bot, tg_id: int):
    user = await bot.get_chat(tg_id)
    res = '<b>Владелец: </b>' + f"@{user.username}"
    return res
    #return f"\n<b>Пользователь:</b> @{username}\n<b>Город:</b> {city}"


async def volunteer_notification_to_owners(bot: Bot, volunteer: Volunteer):
    txt = f"<b>Зарегестрирован новый волонтёр!</b>" + await _get_user_info(bot, volunteer.tg_id)
    for owner_id in OWNERS_ID:
        await bot.send_message(chat_id=owner_id, text=txt, parse_mode='HTML')
        await asyncio.sleep(DELAY_BETWEEN_NOTIFICATIONS_IN_SECONDS)
        
        
async def admin_notification_to_owners(bot: Bot, admin: Admin):
    txt = f"<b>Зарегестрирован новый телеграм канал!</b>" + await _get_user_info(bot, admin.admin_tg_id) + f"\n<b>Название: </b>{admin.channel_name}"
    for owner_id in OWNERS_ID:
        await bot.send_message(chat_id=owner_id, text=txt, parse_mode='HTML')
        await asyncio.sleep(DELAY_BETWEEN_NOTIFICATIONS_IN_SECONDS)
        
        