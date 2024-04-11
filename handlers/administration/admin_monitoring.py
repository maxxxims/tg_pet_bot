from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from keyboards import *
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from database import volunteer_table, pet_table, admin_table, pet2admin_table
from callbacks import *
from utils import get_corrected_city, make_pet_description
from config import  get_owner_tg_id
from fsm import AdminShowPets
from middlewares import StopProcessMiddleware

async def administration_exit(message: Message, state: FSMContext, *args, **kwargs):
    await message.delete()
    await state.set_state(None)
    await message.answer(text='Поиск завершен')

router = Router()
router.message.middleware(StopProcessMiddleware(exit_action=administration_exit))


@router.callback_query(StateFilter(None), AdministrationShowPetsCallback.filter())
async def get_pets_for_admin(query: CallbackQuery, state: FSMContext, callback_data: AdministrationShowPetsCallback):
    if query.from_user.id not in [1737030496, 683099207, 1013170672, 272240371, 353007395]:
        await query.answer(text='Доступно только администраторам', show_alert=False)
        return
    kb = get_kb_choose_city_to_admin()
    await query.message.answer(text='В каком городе показать питомцев?\nЕсли хотите завершить поиск, введите команду /exit', reply_markup=kb)
    await state.set_state(AdminShowPets.choosing_city)
    await query.message.delete()
    

@router.message(AdminShowPets.choosing_city, F.text)
async def administration_first_card(message: Message, state: FSMContext, city: str = None):
    await message.delete()
    #if message.from_user.id not in [1737030496, 683099207, 1013170672, 272240371, 353007395]:
    #    message.answer(text='Доступно только администраторам', show_alert=False)
    #    return
    
    if city is None:
        city = get_corrected_city(message.text)
        if len(city) == 0:
            await message.answer(text='Введите правильное название города или /exit, если хотите завершить поиск')
            return 
        pet = await pet_table.get_available_pet_in_city(city, offset=0)

    else:
        if city == 'any':
            pet = await pet_table.get_available_pet(offset=0)
        else:
            city = get_corrected_city(city)
            pet = await pet_table.get_available_pet_in_city(city, offset=0)
    await state.set_state(None)
    if pet is None:
        await message.answer(text='Больше нет доступных питомцев')
        return
    description = await make_pet_description(pet, to_admin=False, bot=message.bot)
    keyboard = get_kb_navigation_for_administration(city=city, offset=0)
    await message.answer_photo(
        photo=pet.pet_photo_id,
        caption=description,
        parse_mode="HTML",
        reply_markup=keyboard
    )



@router.callback_query(StateFilter(AdminShowPets.choosing_city), AdministrationChooseAnyCityCallback.filter())
async def get_pets_for_admin(query: CallbackQuery, state: FSMContext, callback_data: AdministrationChooseAnyCityCallback):
    await administration_first_card(query.message, state, city='any')
    #await query.message.delete()


@router.callback_query(StateFilter(None), AdministrationNavigationButtonCallback.filter())
async def show_cards_for_administration(query: CallbackQuery, state: FSMContext, callback_data: AdministrationNavigationButtonCallback):    
    new_offset = callback_data.offset + callback_data.ofsset_delta
    if callback_data.city != 'any':
        pet = await pet_table.get_available_pet_in_city(callback_data.city, offset=new_offset)
    else:
        pet = await pet_table.get_available_pet(offset=new_offset)
    if pet is None:
        await query.answer(text='Больше нет  доступных питомцев!', show_alert=True)
        return
    
    await query.message.delete()
    description = await make_pet_description(pet, to_admin=False, bot=query.bot)
    keyboard = get_kb_navigation_for_administration(city=callback_data.city, offset=new_offset)
    await query.message.answer_photo(
        photo=pet.pet_photo_id,
        caption=description,
        parse_mode="HTML",
        reply_markup=keyboard
    )


@router.callback_query(StateFilter(None), AdministrationStopNavigationCallback.filter())
async def stop_administration_navigation(query: CallbackQuery, state: FSMContext):
    await query.message.delete()