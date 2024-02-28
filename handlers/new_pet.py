from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ContentType
from keyboards import * #get_agree_description_kb, get_pet_kb
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from fsm import AddPet
from callbacks import * #PetTypeCallback, AgreeDescriptionCallback
from database import pet_table, volunteer_table
from gpt import make_description
from models import Pet
from utils import make_pet_description, get_corrected_city
from send_notification import send_pet_card_to_admins
from config import MSG_PET_DESCRIPTION
from middlewares import AddUserNameMiddleware, AddingPetMiddleware, AddingPetSkipTextMiddleware

skip_text_router = Router()


router = Router()
router.callback_query.middleware(AddingPetMiddleware())
router.message.middleware(AddingPetSkipTextMiddleware(
    allowed_text_states=[AddPet.choosing_pet_name, AddPet.choosing_pet_age, AddPet.choosing_pet_weight,
                         AddPet.choosing_pet_vaccinations, AddPet.choosing_pet_special_care, 
                         AddPet.choosing_pet_city, AddPet.choosing_pet_promt, AddPet.writing_own_description
                         ]
))




@router.callback_query(AddPet.choosing_pet_type, PetTypeCallback.filter())
async def choose_pet_gender(query: CallbackQuery, state: FSMContext,
                            callback_data: PetTypeCallback, uuid: UUID, from_callback: bool = False):
    if hasattr(callback_data, 'pet_type'):
        if callback_data.pet_type == 'dog':
            smile = "🐕"
        else:
            smile = "🐈"
    else:
        smile = ''
    await query.message.answer(text=f'Укажите пол питомца {smile}', reply_markup=get_choosing_gender_kb())
    await state.set_state(AddPet.choosing_pet_gender)
    if not from_callback:
        await pet_table.update_pet_type(callback_data.pet_type, callback_data.uuid)



@router.callback_query(AddPet.choosing_pet_gender, PetGenderCallback.filter())
async def choose_pet_name(query: CallbackQuery, state: FSMContext,
                          callback_data: PetGenderCallback, uuid: UUID, from_callback: bool = False):
    kb = get_skip_button_and_back(back_stage='choose_pet_gender', foward_stage='choose_pet_age')
    msg = await query.message.answer(text=f'Какая кличка у питомца?',
                               reply_markup=kb)
    await state.set_state(AddPet.choosing_pet_name)
    if not from_callback:
        await pet_table.update_pet_column(uuid, gender=callback_data.pet_gender)
    return msg

    
@router.message(AddPet.choosing_pet_name, F.text)
async def choose_pet_age(message: Message, state: FSMContext,
                           uuid: UUID, from_callback: bool = False):
    kb = get_skip_button_and_back(back_stage='choose_pet_name', foward_stage='choose_pet_weight')
    msg = await message.answer(text=f'Укажите возраст питомца \nНапример, 3 месяца, 2.5 года',
                         reply_markup=kb)
    await state.set_state(AddPet.choosing_pet_age)
    if not from_callback:
        await pet_table.update_pet_column(uuid, name=message.text)
    return msg


@router.message(AddPet.choosing_pet_age, F.text)
async def choose_pet_weight(message: Message, state: FSMContext, uuid: UUID, from_callback: bool = False):
    #kb = get_skip_button(SkipButtonCallback)
    kb = get_skip_button_and_back(back_stage='choose_pet_age', foward_stage='choose_pet_chip')
    msg = await message.answer(text=f'Укажите вес питомца \nНапример, 2 кг', reply_markup=kb)
    await state.set_state(AddPet.choosing_pet_weight)
    if not from_callback:
        await pet_table.update_pet_column(uuid, age=message.text)
    return msg


@router.message(AddPet.choosing_pet_weight, F.text)
async def choose_pet_chip(message: Message, state: FSMContext, uuid: UUID, from_callback: bool = False):
    await message.answer(text=f'Питомец чипирован?', reply_markup=get_choosing_chip_kb())
    await state.set_state(AddPet.choosing_pet_chip)
    if not from_callback:
        await pet_table.update_pet_column(uuid, weight=message.text)
    

@router.callback_query(AddPet.choosing_pet_chip, PetChipCallback.filter())
async def choose_pet_vaccinations(query: CallbackQuery, state: FSMContext, uuid: UUID,
                                   callback_data: PetChipCallback, from_callback: bool = False):
    kb = get_skip_button_and_back(back_stage='choose_pet_chip', foward_stage='choose_pet_castration')
    msg = await query.message.answer(text=f'Укажите информацию о прививках',
                               reply_markup=kb)
    await state.set_state(AddPet.choosing_pet_vaccinations)
    if not from_callback:
        await pet_table.update_pet_column(uuid, has_chip=callback_data.pet_chip)
    return msg


@router.message(AddPet.choosing_pet_vaccinations, F.text)
async def choose_pet_castration(message: Message, state: FSMContext, uuid: UUID, from_callback: bool = False):
    await message.answer(text=f'Кастрация / стерилизация', reply_markup=get_choosing_castration_kb())
    await state.set_state(AddPet.choosing_pet_castration)
    if from_callback:
        return
    await pet_table.update_pet_column(uuid, vaccinations=message.text)


@router.callback_query(AddPet.choosing_pet_castration, PetCastrationCallback.filter())
async def choose_pet_special_care(query: CallbackQuery, state: FSMContext, uuid: UUID,
                                   callback_data: PetCastrationCallback, from_callback: bool = False):
    # print(f'AND HERE!')
    kb = get_skip_button_and_back(back_stage='choose_pet_castration', 
                                  foward_stage='choose_pet_city', foward_text='Не требуется')
    msg = await query.message.answer(text=f'Укажите информацию об особом уходе, если необходимо',
                               reply_markup=kb)
    await state.set_state(AddPet.choosing_pet_special_care)
    if not from_callback:
        await pet_table.update_pet_column(uuid, castration=callback_data.pet_castration)
    return msg


@router.message(AddPet.choosing_pet_special_care, F.text)
async def choose_pet_city(message: Message, state: FSMContext,
                                 uuid: UUID, from_callback: bool = False, user_id: int = None):    
    if not from_callback:
        user_id = message.from_user.id
    default_city = await volunteer_table.get_volunteer_city(user_id)
    print(f'city = {default_city}')
    print('\n' * 5)
    msg = await message.answer(text='Введите город, в котором находится питомец',
                         reply_markup=get_choosing_default_city_kb(default_city=default_city))
    await state.set_state(AddPet.choosing_pet_city)
    if from_callback:
        return msg
    await pet_table.update_pet_column(uuid, special_care=message.text)
    return msg

@router.callback_query(AddPet.choosing_pet_city, PetCityCallback.filter())
async def choose_pet_city_callback(query: CallbackQuery, state: FSMContext,
                                   uuid:UUID, callback_data: PetCityCallback):
    await state.set_state(AddPet.choosing_pet_photo)
    await choose_pet_photo(query.message, state, uuid=uuid, from_callback=True, default_city=callback_data.pet_city)


@router.message(AddPet.choosing_pet_city, F.text)
async def choose_pet_photo(message: Message, state: FSMContext, uuid: UUID,
                           from_callback: bool = False, default_city: str = None):
    if from_callback:
        corrected_city = default_city
    else: 
        corrected_city = get_corrected_city(message.text)
    print('\n'* 3)
    print(f'city = {corrected_city}')
    print('\n'* 3)
    if len(corrected_city) == 0:
        await message.answer(text='Некорректное название города')
        return
    
    await pet_table.update_pet_column(uuid, city=corrected_city)
    kb = get_kb_for_photo()
    msg = await message.answer(text=f'Отправьте фото питомца. Пожалуйста, отправьте как фото, а не как прикреплённый файл', reply_markup=kb)
    await state.set_state(AddPet.choosing_pet_photo)
    return msg


@router.message(AddPet.choosing_pet_photo, F.photo)
async def chose_pet_description(message: Message, state: FSMContext, uuid: UUID, from_callback: bool = False):
    #message.bot.delete_message(message.chat.id, message.message_id)
    photos = message.photo
    for photo in photos:
        photo_id = photo.file_id
        break
    if not from_callback:
        await pet_table.update_pet_photo(photo_id, uuid)
    kb = get_kb_for_description()
    await message.answer(text='Отправьте описание питомца', reply_markup=kb)
    await state.set_state(AddPet.choosing_pet_promt)


@router.message(AddPet.choosing_pet_promt, F.text)
async def make_prompt(message: Message, state: FSMContext, uuid: UUID):
    prompt = message.text
    await pet_table.update_pet_prompt(prompt, uuid)
    pet = await pet_table.get_info_from_pet(uuid)
    sent_msg = await message.answer(text='Создаем описание...✏️')
    description = await make_description(pet) #message.text #+ 'description'

    await pet_table.update_pet_description(description, uuid)
    await message.answer(text=f'{description}',
                         )
    await message.answer(text=MSG_PET_DESCRIPTION,
        reply_markup=get_agree_description_kb()
    )
    await sent_msg.delete()



@router.callback_query(AddPet.choosing_pet_promt, AgreeDescriptionCallback.filter())
async def agree_prompt(query: CallbackQuery, state: FSMContext, uuid:UUID,
                        callback_data: AgreeDescriptionCallback):
    if callback_data.agree:
        await pet_table.update_available_pet(available=True, uuid=uuid)
        pet = await pet_table.get_info_from_pet(uuid)
        text = '<u><b>Карточка питомца:</b></u> \n' + make_pet_description(pet)
        await query.message.answer_photo(pet.pet_photo_id,
                                        caption=text,
                                        parse_mode="HTML")
        await state.set_state(None)

        if pet.city is not None:
            await send_pet_card_to_admins(query.bot, pet, pet.city)
            #await send_notification_in_one_city(query.bot, pet.city)

    else:
        await query.answer()
        pet = await pet_table.get_info_from_pet(uuid)
        sent_msg = await query.message.answer(text='Создаем описание...✏️')
        new_description = await make_description(pet) #message.text #+ 'description'

        await pet_table.update_pet_description(new_description, uuid)
        await query.message.answer(text=f'{new_description}')

        await query.message.answer(
            text=MSG_PET_DESCRIPTION, reply_markup=get_agree_description_kb()
        )

        await sent_msg.delete()


@router.callback_query(AddPet.choosing_pet_promt, WriteOwnDescriptionCallback.filter())
async def write_own_description(query: CallbackQuery, state: FSMContext, uuid: UUID,
                                 callback_data: WriteOwnDescriptionCallback):
    await query.message.answer(
        text='<b>Введите описание питомца</b>',
        parse_mode='HTML'
    )
    await state.set_state(AddPet.writing_own_description)
    await query.answer()
    # await query.message.delete()


@router.message(AddPet.writing_own_description, F.text)
async def write_own_description_text(message: Message, state: FSMContext, uuid: UUID):
    description = message.text
    await pet_table.update_pet_description(description, uuid)
    await message.answer(
        text='Введите описание питомца'
    )
    await pet_table.update_available_pet(available=True, uuid=uuid)
    pet = await pet_table.get_info_from_pet(uuid)
    text = '<u><b>Карточка питомца:</b></u>\n' + make_pet_description(pet)
    await message.answer_photo(pet.pet_photo_id,
                                    caption=text,
                                    parse_mode="HTML")
    await state.set_state(None)

    if pet.city is not None:
        await send_pet_card_to_admins(message.bot, pet, pet.city)


@router.callback_query(
    StateFilter(*AddPet.get_all_states()), SkipRegistrationStageCallback.filter()
)        
async def previous_stage(query: CallbackQuery, state: FSMContext,
                        callback_data: SkipRegistrationStageCallback, uuid: UUID):
    print(f'calback_data = {callback_data}')
    if callback_data.new_stage == 'choose_pet_gender':
        msg = await choose_pet_gender(query, state, callback_data, uuid, from_callback=True)
    elif callback_data.new_stage == 'choose_pet_name':
        msg = await choose_pet_name(query, state, callback_data, uuid, from_callback=True)
    elif callback_data.new_stage == 'choose_pet_age':
        # print('HERE!')
        msg = await choose_pet_age(query.message, state, uuid, from_callback=True)
    elif callback_data.new_stage == 'choose_pet_weight':
        msg = await choose_pet_weight(query.message, state, uuid, from_callback=True)
    elif callback_data.new_stage == 'choose_pet_chip':
        msg = await choose_pet_chip(query.message, state, uuid, from_callback=True)
    elif callback_data.new_stage == 'choose_pet_vaccinations':
        msg = await choose_pet_vaccinations(query, state, callback_data, uuid, from_callback=True)
    elif callback_data.new_stage == 'choose_pet_castration':
        msg = await choose_pet_castration(query.message, state, uuid, from_callback=True)
    elif callback_data.new_stage == 'choose_pet_special_care':
        print(f'HERE!!!!!!!!!!')
        msg = await choose_pet_special_care(query, state, callback_data, uuid, from_callback=True)
    elif callback_data.new_stage == 'choose_pet_city':
        user_id = query.from_user.id
        msg = await choose_pet_city(query.message, state, uuid, from_callback=True, user_id=user_id)
    elif callback_data.new_stage == 'choose_pet_photo':
        user_id = query.from_user.id
        default_city = await volunteer_table.get_volunteer_city(user_id)
        msg = await choose_pet_photo(query.message, state, uuid, from_callback=True, default_city=default_city)
    #elif callback_data.new_stage == 'choose_pet_vaccinations':
    #    await choose_pet_vaccinations(query, state, callback_data, uuid=uuid, from_callback=True)
    # await query.message.delete()
    await query.answer()
    return msg


@router.message(StateFilter(*AddPet.get_all_states()))
async def skip_text(message: Message, state: FSMContext, uuid: UUID):
    print('here!!!!!!!!')
    await message.delete()
    ...