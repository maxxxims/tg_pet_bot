from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ContentType
from keyboards import get_choosing_type_of_my_pets, get_kb_for_notification, get_navigation_kb_for_volunteer
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from database import volunteer_table, pet_table, admin_table
from callbacks import *
from utils import make_pet_description, navigation_button_function


router = Router()


MSG = "Список доступных команд: \n/dog - поиск собаки\n/cat - поиск кошки\n/new - добавить питомца"


@router.message(StateFilter(None), Command('pets'))
async def cmd_pets(message: Message, state: FSMContext):
    kb = get_choosing_type_of_my_pets()
    await message.answer(text='Выберите необходимый пункт', reply_markup=kb)
    # await message.answer(text = f'{message.from_user.username} and @{message.from_user.username},')
    # await message.answer(text = f'<a href="tg://user?id={message.from_user.id}">USER</a> ,')
    # await message.answer(text = f'<a href="https://t.me/{message.from_user.username}">USER</a> ,')


@router.callback_query(StateFilter(None), ShowVolunteerPetsCallback.filter())
async def show_volunteer_pets(query: CallbackQuery, state: FSMContext, callback_data: ShowVolunteerPetsCallback):
    is_volunteer = await volunteer_table.is_volounteer(query.from_user.id)
    if not is_volunteer:
        await query.answer(text='Вы не являетесь волонтером', show_alert=False)
        return
    
    pet = await pet_table.get_volinteer_pets(query.from_user.id, offset=0)

    if pet is None:
        await query.answer(text='Вы не добавили ни одного питомца!', show_alert=True)
        await query.message.delete()
        return
    description = make_pet_description(pet)
    # keyboard = get_kb_for_notification(pet_type='any', offset=0)
    keyboard = get_navigation_kb_for_volunteer(uuid=pet.uuid, offset=0)
    await query.message.answer_photo(
        photo=pet.pet_photo_id,
        caption=description,
        parse_mode="HTML",
        reply_markup=keyboard
    )

    await query.message.delete()


@router.callback_query(StateFilter(None), NavigationButtonCallback.filter(F.send_to == 'volunteer'))
async def show_notifications_volunteer(query: CallbackQuery, state: FSMContext, callback_data: NavigationButtonCallback):
    is_volunteer = await volunteer_table.is_volounteer(query.from_user.id)
    if not is_volunteer:
        await query.answer(text='Вы не являетесь волонтером', show_alert=False)
        return
    
    new_offset = callback_data.offset + callback_data.ofsset_delta
    pet = await pet_table.get_volinteer_pets(query.from_user.id, offset=new_offset)
    
    if pet is None:
        await query.answer(text='Больше нет добавленных питомцев!', show_alert=True)
        return

    keyboard = get_navigation_kb_for_volunteer(uuid=pet.uuid, offset=new_offset)

    await navigation_button_function(query, callback_data, keyboard, pet, new_offset=new_offset)
    await query.answer()


@router.callback_query(StateFilter(None), DeleteVolunteerPetCallback.filter())
async def delete_volunteer_pets(query: CallbackQuery, state: FSMContext, callback_data: DeleteVolunteerPetCallback):
    #is_volunteer = await volunteer_table.is_volounteer(query.from_user.id)
    #if not is_volunteer:
    # ??????????????????????
    await query.message.delete()
    await pet_table.delete_pet_card(callback_data.uuid)
    await query.answer(text='Карточка удалена', show_alert=False)

    delta = - 1 if callback_data.current_offset != 0 else 1

    await show_notifications_volunteer(query, state, callback_data=NavigationButtonCallback(
        offset=callback_data.current_offset,
        ofsset_delta=delta, send_to='volunteer'
        ))


##################### ADMIN #######################

@router.callback_query(StateFilter(None), ShowAdminNotificationCallback.filter())
async def show_admin_pets(query: CallbackQuery, state: FSMContext, callback_data: ShowAdminNotificationCallback):
    is_admin = await admin_table.is_admin(query.from_user.id)
    if not is_admin:
        await query.answer(text='Вы не подключили свой телеграмм канал')
        return
    
    city = await admin_table.get_admin_city(query.from_user.id)
    pet = await pet_table.get_available_pet_in_city(city, offset=0)
    await query.message.delete()

    if pet is None:
        await query.answer(text='Нет доступных питомцев', show_alert=True)
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


@router.callback_query(StateFilter(None), NavigationButtonCallback.filter(F.send_to == 'admin'))
async def show_notifications_any(query: CallbackQuery, state: FSMContext, callback_data: NavigationButtonCallback):
    city = await admin_table.get_admin_city(query.from_user.id)
    if city is None:
        await query.answer()
        return
    new_offset = callback_data.offset + callback_data.ofsset_delta
    pet = await pet_table.get_available_pet_in_city(city, offset=new_offset)
    
    # await query.message.delete()
    #keyboard = get_pet_navigation_kb(pet_type=callback_data.pet_type, offset=new_offset, uuid=pet.uuid)

    keyboard = get_kb_for_notification(send_to='admin', offset=new_offset)
    # else:
    #     keyboard = get_navigation_kb_for_volunteer(uuid=pet.uuid, offset=new_offset)

    await navigation_button_function(query, callback_data, keyboard, pet, new_offset=new_offset)
    await query.answer()

    


########################################
# FOR ALL
##########################################
@router.callback_query(StateFilter(None), StopNavigationCallback.filter())
async def stop_notifications(query: CallbackQuery, state: FSMContext, callback_data: MyPetsCloseCallback):
    await query.message.delete()
    await query.answer()

