from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ContentType
from keyboards import get_agree_description_kb, get_pet_kb
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from fsm import VolunteerRegistration, AdminRegistration
from callbacks import PetTypeCallback, AgreeDescriptionCallback, RegistrationProfileTypeCallback
from database import admin_table
from utils import validate_city, get_corrected_city
from config import MSG_AFTER_ADMIN_REGISTRATION
from middlewares import StopProcessMiddleware



async def exit_action_admin_registration(message: Message, state: FSMContext, *args, **kwargs):
    await message.answer(text='Регистрация остановлена')
    await state.set_state(None)
    await admin_table.delete_admin(message.from_user.id)


router = Router()
router.message.middleware(StopProcessMiddleware(exit_action=exit_action_admin_registration))


@router.callback_query(StateFilter(None), RegistrationProfileTypeCallback.filter(F.profile_type == 'admin'))
async def cmd_registration_admin(query: CallbackQuery, state: FSMContext, callback_data: RegistrationProfileTypeCallback):
    if await admin_table.is_admin(query.from_user.id):
        await query.answer(text='Вы уже зарегистрированы как администратор канала')
        return
    await admin_table.add_admin(query.from_user.id, query.from_user.full_name, query.from_user.username)
    await query.message.answer(text='Если вы хотите остановить регистрацию, введите команду /exit')
    await query.message.answer(text='Введите название канала')
    await state.set_state(AdminRegistration.writing_channel_name)
    await query.message.delete()
    await query.answer()





@router.message(AdminRegistration.writing_channel_name, F.text)
async def cmd_registration_admin_channel(message: Message, state: FSMContext):
    if message.text is None or message.text.startswith('/'):
        await message.answer(text='Введите правильное название канала')
        return
    channel_name = message.text
    await admin_table.update_admin_column(message.from_user.id, channel_name=channel_name)
    await message.answer(text='Введите город, на который ориентирован канал')
    await state.set_state(AdminRegistration.writing_city)


@router.message(AdminRegistration.writing_city, F.text)
async def cmd_registration_admin_city(message: Message, state: FSMContext):
    corrected_city = get_corrected_city(message.text)
    if len(corrected_city) == 0:
        await message.answer(text='Введите правильное название города')
        return 
    await message.answer(text=MSG_AFTER_ADMIN_REGISTRATION)
    await admin_table.update_admin_column(message.from_user.id, city=corrected_city)
    await admin_table.finish_registration(message.from_user.id)
    await state.set_state(None)


