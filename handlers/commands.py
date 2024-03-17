from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ContentType, InputFile, FSInputFile
from keyboards import get_pet_navigation_kb, get_profile_type_kb, get_pet_kb
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from database import volunteer_table, statistic, pet_table
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


@router.message(StateFilter(None), Command('registration'))
async def cmd_start_registration(message: Message, state: FSMContext):
    await message.answer(text='Выберите роль для регистрации',
                         reply_markup=get_profile_type_kb())


@router.message(StateFilter(None), Command('new'))
async def cmd_new(message: Message, state: FSMContext, from_callback: bool = False):
    if not from_callback:
        if not await volunteer_table.is_volounteer(message.from_user.id):
            await message.answer(text='Только волонтёры могут добавлять питомцев')
            return
        uuid = await pet_table.add_new_pet(message.from_user.id)
        await state.update_data(uuid=uuid)

    await message.answer(text='Выберите тип питомца',
                         reply_markup=get_pet_kb(uuid=uuid))
    await state.set_state(AddPet.choosing_pet_type)


@router.message(StateFilter(None), Command('statistics'))
async def cmd_statistics(message: Message, state: FSMContext):
    if message.from_user.id in [1737030496, 683099207, 1013170672, 272240371, 353007395]:
        df_pet_table, df_volunteer_table, df_admin_table, df_pet2admin_table = await statistic.get_statistics()

        volunteers_number = len(df_volunteer_table)
        pets_number = len(df_pet_table)
        channels_number = len(df_admin_table)
        
        df_volunteer_table['added_pets_number'] = df_volunteer_table['tg_id'].map(
            lambda x: np.sum(df_pet_table['volunteer_tg_id'] == x))
        
        df_volunteer_table.drop(columns=['tg_id'], inplace=True)

        df_admin_table['reposted_pets'] = df_admin_table['admin_tg_id'].map( lambda row:
            np.sum(df_pet2admin_table['admin_tg_id'] == row)
        )
        df_admin_table.drop(columns=['admin_tg_id'], inplace=True)

        with pd.ExcelWriter("data/statistics.xlsx") as writer:
            df_volunteer_table.to_excel(writer, sheet_name="Волонтёры", index=False)
            df_admin_table.to_excel(writer, sheet_name="Администраторы каналов", index=False)

        caption = f'Зарегистрировано волонтеров: {volunteers_number}\nЗарегистрировано питомцев: {pets_number}\nЗарегистрировано каналов: {channels_number}'
        await message.answer_document(FSInputFile('data/statistics.xlsx'), caption=caption)