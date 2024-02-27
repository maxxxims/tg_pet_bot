from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ContentType
from keyboards import get_pet_navigation_kb, get_kb_for_notification
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from callbacks import NavigationButtonCallback, StopNavigationCallback, ShowPetsCallback, OffNotificationCallback, MyPetsCloseCallback, \
    AdminRepostPetCallback
from database import pet_table, admin_table
from keyboards.manage_pets_kb import get_navigation_kb_for_volunteer 
# from models import Pet
from utils import make_pet_description, navigation_button_function
# from pytz import timezone as tz
# from datetime import datetime, date, timedelta

router = Router()

"""

@router.callback_query(StateFilter(None), ShowPetsCallback.filter())
async def show_notifications(query: CallbackQuery, state: FSMContext, callback_data: ShowPetsCallback):
    pet = await pet_table.get_available_pet_in_city(callback_data.city, offset=0)
    await query.message.delete()

    if pet is None:
        await query.answer(text='Нет доступных питомцев', show_alert=False)
        return
    description = make_pet_description(pet)
    keyboard = get_kb_for_notification(send_to='admin', offset=0)
    await query.message.answer_photo(
        photo=pet.pet_photo_id,
        caption=description,
        parse_mode="HTML",
        reply_markup=keyboard
    )
    await query.answer()



@router.callback_query(StateFilter(None), OffNotificationCallback.filter())
async def stop_notifications(query: CallbackQuery, state: FSMContext, callback_data: OffNotificationCallback):
    #await query
    #await query.message.answer(text='Вы отключили уведомления')
    # await query.message.delete()
    await query.answer(text='Вы отключили уведомления', show_alert=False)

"""
    
@router.callback_query(StateFilter(None), AdminRepostPetCallback.filter())
async def admin_reposted_pet(query: CallbackQuery, state: FSMContext, callback_data: AdminRepostPetCallback):
    #await query
    #await query.message.answer(text='Вы отключили уведомления')
    # await query.message.delete()
    await query.answer(text='Спасибо, вы делаете мир лучше', show_alert=False)
    if callback_data.delete_msg:
        await query.message.delete()


