from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ContentType
from keyboards import get_agree_description_kb, get_pet_kb
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from fsm import AddPet
from callbacks import PetTypeCallback, AgreeDescriptionCallback
from database import pet_table
from datetime import datetime

router = Router()


@router.message(StateFilter(None), Command('new'))
async def cmd_new(message: Message, state: FSMContext):
    # await message.answer(text=f'Выбе {message.date}')
    uuid = await pet_table.add_new_pet(message.from_user.id, message.from_user.full_name)
    data = await state.get_data()
    await state.update_data(uuid=uuid)
    await message.answer(text='Выберите тип питомца',
                         reply_markup=get_pet_kb(uuid=uuid))
    await state.set_state(AddPet.choosing_pet_type)
    

@router.callback_query(AddPet.choosing_pet_type, PetTypeCallback.filter())
async def choose_pet_type(query: CallbackQuery, state: FSMContext, callback_data: PetTypeCallback):
    try:    await query.message.delete()
    except:  ...
    if callback_data.pet_type == 'dog':
        smile = "🐕"
    else:
        smile = "🐈"
    await query.message.answer(text=f'Введите описание питомца {smile}')
    await state.set_state(AddPet.choosing_pet_promt)
    await pet_table.update_pet_type(callback_data.pet_type, callback_data.uuid)


@router.message(AddPet.choosing_pet_promt)
async def make_prompt(message: Message, state: FSMContext):
    prompt = message.text
    description = message.text #+ 'description'
    data = await state.get_data()
    uuid = data['uuid']
    await pet_table.update_pet_prompt(prompt, uuid)
    await pet_table.update_pet_description(description, uuid)
    await message.answer(text=f'Описание питомца: \n{description}',
                         reply_markup=get_agree_description_kb())


@router.callback_query(AddPet.choosing_pet_promt, AgreeDescriptionCallback.filter())
async def agree_prompt(query: CallbackQuery, state: FSMContext, callback_data: PetTypeCallback):
    if callback_data.agree:
        try:    await query.message.delete()
        except:  ...
        await query.message.answer(text='Отправьте фото питомца')
        await state.set_state(AddPet.choosing_pet_photo)
    else:
        data = await state.get_data()
        uuid = data['uuid']
        prompt = await pet_table.get_prompt(uuid)
        description = await pet_table.get_description(uuid)
        new_description = description + '\nтипо новое описание'
        await pet_table.update_pet_description(new_description, uuid)

        try:    await query.message.delete()
        except:  ...

        await query.message.answer(text=f'Ваш текст: \n{new_description}',
                         reply_markup=get_agree_description_kb())


@router.message(AddPet.choosing_pet_photo, F.photo)
async def pick_photo(message: Message, state: FSMContext):
    photos = message.photo
    for photo in photos:
        photo_id = photo.file_id
        break
    data = await state.get_data()
    uuid = data['uuid']
    await pet_table.update_pet_photo(photo_id, uuid)
    await pet_table.update_available_pet(available=True, uuid=uuid)
    await state.set_state(None)
    pet = await pet_table.get_info_from_pet(uuid)

    text = "<b>Карточка питомца:</b> \n" + pet.description

    await message.answer_photo(pet.pet_photo_id, caption=text)
