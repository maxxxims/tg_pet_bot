from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ContentType
from keyboards import get_pet_navigation_kb
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from fsm import AddPet
from callbacks import PetTypeCallback, AgreeDescriptionCallback, NavigationButtonCallback, StopNavigationCallback,\
    AddFavouriteCallback
from database import pet_table
# from models import Pet
from utils import make_pet_description, navigation_button_function
# from pytz import timezone as tz
# from datetime import datetime, date, timedelta

router = Router()


# def make_pet_description(pet: Pet):
#     user_name = f'[{pet.owner_nick}](tg://user?id={str({pet.owner_id})})'
#     text = pet.description + '\n' + 'Владелец: ' + f'[{pet.owner_nick}](tg://user?id={str(pet.owner_id)})'
#     return text

#    # await message.answer(text=f'[{message.from_user.full_name}](tg://user?id={str(message.from_user.id)}), @{message.from_user.full_name}',
    #                     parse_mode="Markdown")

@router.message(StateFilter(None), Command('dog'))
async def cmd_dog(message: Message, state: FSMContext):
    pet = await pet_table.get_available_pet('dog', offset=0)
    if pet is None:
        await message.answer(text='Нет доступных питомцев')
        return
    description = make_pet_description(pet)
    await message.answer_photo(
        photo=pet.pet_photo_id,
        caption=description,
        parse_mode="HTML",
        reply_markup=get_pet_navigation_kb(pet_type='dog', offset=0, uuid=pet.uuid)
    )


@router.message(StateFilter(None), Command('cat'))
async def cmd_dog(message: Message, state: FSMContext):
    pet = await pet_table.get_available_pet('cat', offset=0)
    if pet is None:
        await message.answer(text='Нет доступных питомцев')
        return
    description = make_pet_description(pet)
    await message.answer_photo(
        photo=pet.pet_photo_id,
        caption=description,
        parse_mode="HTML",
        reply_markup=get_pet_navigation_kb(pet_type='cat', offset=0, uuid=pet.uuid)
    )


@router.callback_query(StateFilter(None), NavigationButtonCallback.filter(F.pet_type != 'any'))
async def navigation_button(query: CallbackQuery, state: FSMContext, callback_data: NavigationButtonCallback):
    new_offset = callback_data.offset + callback_data.ofsset_delta
    pet = await pet_table.get_available_pet(callback_data.pet_type, offset=new_offset)
    keyboard = get_pet_navigation_kb(pet_type=callback_data.pet_type, offset=new_offset, uuid=pet.uuid)
    await navigation_button_function(query, callback_data, keyboard, pet, new_offset=new_offset)
    # if pet is None:
    #     await query.message.answer(text='Больше нет доступных питомцев')
    #     await query.answer()
    #     return
    # description = make_pet_description(pet)
    # try:    await query.message.delete()
    # except:  ...
    # await query.message.answer_photo(
    #     photo=pet.pet_photo_id,
    #     caption=description,
    #     parse_mode="HTML",
    #     reply_markup=get_pet_navigation_kb(pet_type=callback_data.pet_type, offset=new_offset, uuid=pet.uuid)
    # )
    # await query.answer()


@router.callback_query(StateFilter(None), StopNavigationCallback.filter())
async def stop_navigation(query: CallbackQuery, state: FSMContext, callback_data: PetTypeCallback):
    try:    await query.message.delete()
    except:  ...



@router.callback_query(StateFilter(None), AddFavouriteCallback.filter())
async def stop_navigation(query: CallbackQuery, state: FSMContext, callback_data: PetTypeCallback):
    # delta: timedelta = query.message.date - datetime.utcnow().replace(tzinfo=tz('UTC'))
    # print(f'{delta}')
    # print(f'{delta.days}')
    # print(f'sec = {delta.seconds}')
    # print(f'minutes = {delta.seconds / 60}')
    await query.message.answer(text='Питомец добавлен в избранное❤️')
    await query.answer()
    # try:    await query.message.delete()
    # except:  ...
