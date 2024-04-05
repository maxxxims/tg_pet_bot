from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ContentType
from keyboards import get_agree_description_kb, get_pet_kb
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from fsm import VolunteerRegistration, AdminRegistration
from callbacks import PetTypeCallback, AgreeDescriptionCallback, RegistrationProfileTypeCallback
from database import volunteer_table
from datetime import datetime
from gpt import make_description
from models import Volunteer
from utils import validate_phone_number, get_corrected_city
from send_notification import volunteer_notification_to_owners
from config import MSG_AFTER_REGISTRATION
import logging

logging.basicConfig(level=logging.INFO)

router = Router()


#MSG_AFTER_REGISTRATION = "Список доступных команд: \n/new - добавить питомца \n/dog - поиск собаки\n/cat - поиск кошки\n"




@router.callback_query(StateFilter(None), RegistrationProfileTypeCallback.filter(F.profile_type == 'volunteer'))
async def cmd_registration_volounteer(query: CallbackQuery, state: FSMContext, callback_data: RegistrationProfileTypeCallback):
    if await volunteer_table.is_volounteer(query.from_user.id):
        await query.answer(text='Вы уже зарегистрированы как волонтёр')
        return
    await volunteer_table.add_volounteer(query.from_user.id, query.from_user.full_name)
    await volunteer_table.update_column(query.from_user.id, username=query.from_user.username)
    await query.message.answer(text='Введите Ваше имя')
    await state.set_state(VolunteerRegistration.writing_name)
    await query.message.delete()
    await query.answer()

# @router.message(VolunteerRegistration.writing_name, F.text)
# async def writing_name(message: Message, state: FSMContext):
#     if message.text.startswith('/'):
#         await message.answer(text='Пожалуйста завершите регистрацию для дальнейшего использования команд')
#         return
#     await volunteer_table.update_name(message.from_user.id, message.text)
#     await message.answer(text='Введите Вашу фамилию')
#     await state.set_state(VolunteerRegistration.writing_surname)


@router.message(VolunteerRegistration.writing_name, F.text)
async def writing_name(message: Message, state: FSMContext):
    if message.text.startswith('/'):
        await message.answer(text='Пожалуйста завершите регистрацию для дальнейшего использования команд')
        return
    await volunteer_table.update_name(message.from_user.id, message.text)
    await message.answer(text='Введите номер телефона')
    await state.set_state(VolunteerRegistration.writing_phone)


@router.message(VolunteerRegistration.writing_phone, F.text)
async def writing_phone(message: Message, state: FSMContext):
    if message.text.startswith('/'):
        await message.answer(text='Пожалуйста завершите регистрацию для дальнейшего использования команд')
        return
    phone_number = str(message.text)
    number_is_correct = validate_phone_number(phone_number)
    if number_is_correct:
        await volunteer_table.update_phone(message.from_user.id, message.text.replace(' ', ''))
        await message.answer(text='Введите город')
        await state.set_state(VolunteerRegistration.writing_city)
    else:
        await message.answer(text='Некорректный номер телефона. \nНомер должен начинаться с 8 или +7')


@router.message(VolunteerRegistration.writing_city, F.text)
async def writing_city(message: Message, state: FSMContext):
    if message.text.startswith('/'):
        await message.answer(text='Пожалуйста завершите регистрацию для дальнейшего использования команд')
        return
    #city_is_correct = validate_city(message.text)
    corrected_city = get_corrected_city(message.text)
    if len(corrected_city) == 0:
        await message.answer(text='Такой город не найден. Введите еще раз')
        return
    await volunteer_table.update_city(message.from_user.id, corrected_city)
    await volunteer_table.finish_registration(message.from_user.id)
    await message.answer(text='Поздравляем, регистрация завершена!' + '\n' + MSG_AFTER_REGISTRATION)
    #await message.answer(text=MSG_AFTER_REGISTRATION)
    await state.set_state(None)
    
    volunteer = await volunteer_table.get_volunteer(message.from_user.id)
    #logging.info(f'VOLUNTEER, REGISTRED!, user_id = {message.from_user.id}; username = {volunteer.username}')
    await volunteer_notification_to_owners(message.bot, volunteer)