from config import DELAY_BETWEEN_NOTIFICATIONS_IN_SECONDS, DEFAULT_NOTIFICATION_TO_ADMIN
import asyncio
from aiogram.types import Message
from aiogram import Bot
from models import Admin
from keyboards import get_show_notification_kb, get_notification_kb_for_admin
from database import admin_table, pet2admin_table
from models import Pet
from utils import make_pet_description



async def send_feedback_to_volunteer(bot: Bot, volunteer_tg_id: int, pet_photo_id: str):
    text = 'Опубликована карточка вашего питомца!'
    await bot.send_photo(chat_id=volunteer_tg_id, photo=pet_photo_id, caption=text)