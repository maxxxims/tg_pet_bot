from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ContentType
from keyboards import get_agree_description_kb, get_pet_kb

from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from fsm import VolunteerRegistration, AdminRegistration
from callbacks import PetTypeCallback, AgreeDescriptionCallback, RegistrationProfileTypeCallback
from database import admin_table
from models import Volunteer
from utils import validate_city, get_corrected_city
from config import MSG_AFTER_ADMIN_REGISTRATION
# import asyncio
# from send_notification import send_notification_in_one_city

router = Router()




@router.callback_query(StateFilter(None), RegistrationProfileTypeCallback.filter(F.profile_type == 'admin'))
async def cmd_registration_admin(query: CallbackQuery, state: FSMContext, callback_data: RegistrationProfileTypeCallback):
    #await query.message.answer(f'ваш айди = {query.from_user.id}')
    if await admin_table.is_admin(query.from_user.id):
        await query.answer(text='Вы уже зарегистрированы как администратор канала')
        return
    print(f'user id = {query.message.from_user.id}; user full name = {query.message.from_user.full_name}')
    await admin_table.add_admin(query.from_user.id, query.from_user.full_name)
    await query.message.answer(text='Введите название канала')
    await state.set_state(AdminRegistration.writing_channel_name)
    await query.message.delete()
    await query.answer()


@router.message(AdminRegistration.writing_channel_name, F.text)
async def cmd_registration_admin_channel(message: Message, state: FSMContext):
    if message.text is None or message.text.startswith('/'):
        await message.answer(text='Введите правильное название канала')
        return
    #await volunteer_table.add_volounteer(query.message.from_user.id, query.message.from_user.full_name)
    channel_name = message.text
    await admin_table.update_admin_column(message.from_user.id, channel_name=channel_name)
    await message.answer(text='Введите город, на который ориентирован канал')
    await state.set_state(AdminRegistration.writing_city)


@router.message(AdminRegistration.writing_city, F.text)
async def cmd_registration_admin_city(message: Message, state: FSMContext):
    # if validate_city(message.text) or message.text.startswith('/'):
    #     await message.answer(text='Введите правильное название города')
    #     return
    print(f'validate city = {validate_city(message.text)}')
    corrected_city = get_corrected_city(message.text)
    if len(corrected_city) == 0:
        await message.answer(text='Введите правильное название города')
        return 
    await message.answer(text=MSG_AFTER_ADMIN_REGISTRATION)
    await admin_table.update_admin_column(message.from_user.id, city=corrected_city)
    await admin_table.finish_registration(message.from_user.id)
    await state.set_state(None)

    # await test(message)
    # await asyncio.sleep(10)
    # await message.answer(text='А я не сплю!')
    # await asyncio.sleep(10)
    # await message.answer(text='А я не сплю все еще!')