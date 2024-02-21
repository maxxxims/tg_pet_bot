from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ContentType, InputFile, FSInputFile
from keyboards import get_pet_navigation_kb, get_profile_type_kb
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from database import volunteer_table, statistic
from fsm import VolunteerRegistration, AddPet
from aiogram.methods import SendMessage
import numpy as np
import pandas as pd

router = Router()


MSG = "Список доступных команд: \n/registration - регистрация \n/pets - просмотр питомцев\n/statistics - просмотр статистики"


@router.message(StateFilter(None), Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    print(f'INSTANSE = {type(state)}, {isinstance(state, AddPet)}')
    await message.answer(text=MSG)


@router.message(StateFilter(None), Command('info'))
async def cmd_info(message: Message, state: FSMContext):
    await message.answer(text=MSG)

# @router.message(StateFilter(None), Command('info'))
# async def cmd_info(message: Message, state: FSMContext):
#     await message.answer(text=MSG + f'message.chat.id = {message.chat.id}, id = {message.from_user.id}')
#     #await message.bot.send_message(chat_id=6161416635, text="тестовое сообщение от бота")
#     user_channel_status = await message.bot.get_chat_member(chat_id='-1002026863689', user_id=message.from_user.id)
#     user_channel_status_admins = await message.bot.get_chat_administrators(chat_id='-1002026863689')
#     # message.bot.
#     print('*****************************')
#     print(user_channel_status)
#     print('*****************************')
#     print(user_channel_status_admins)
    

@router.message(StateFilter(None), Command('registration'))
async def cmd_start_registration(message: Message, state: FSMContext):
    await message.answer(text='Выберите роль для регистрации',
                         reply_markup=get_profile_type_kb())



@router.message(StateFilter(None), Command('statistics'))
async def cmd_statistics(message: Message, state: FSMContext):
    df_pet_table, df_volunteer_table, df_admin_table = await statistic.get_statistics()

    volunteers_number = len(df_volunteer_table)
    pets_number = len(df_pet_table)
    channels_number = len(df_admin_table)
    
    df_volunteer_table['added_pets_number'] = df_volunteer_table['tg_id'].map(
        lambda x: np.sum(df_pet_table['volunteer_tg_id'] == x))
    
    df_volunteer_table.drop(columns=['tg_id'], inplace=True)

    # await message.answer(
    #     text=f'Зарегистрировано волонтеров: {volunteers_number}\nЗарегистрировано питомцев: {pets_number}\nЗарегистрировано каналов: {channels_number}'
    # )

    with pd.ExcelWriter("data/statistics.xlsx") as writer:
        df_volunteer_table.to_excel(writer, sheet_name="Волонтёры", index=False)
        df_admin_table.to_excel(writer, sheet_name="Администраторы каналов", index=False)

    caption = f'Зарегистрировано волонтеров: {volunteers_number}\nЗарегистрировано питомцев: {pets_number}\nЗарегистрировано каналов: {channels_number}'
    await message.answer_document(FSInputFile('data/statistics.xlsx'), caption=caption)