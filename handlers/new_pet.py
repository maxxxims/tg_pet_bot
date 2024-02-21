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

router = Router()


# def make_pet_description(pet: Pet):
#     user_name = f'[{pet.volunteer.nick}](tg://user?id={str({pet.volunteer_tg_id})})'
#     #user_name = f'[{pet.owner_nick}](tg://user?id={str({pet.owner_id})})'
#     text = pet.description + '\n' + 'Владелец: ' + f'[{pet.volunteer.nick}](tg://user?id={str(pet.volunteer_tg_id)})'
#     return text


@router.message(StateFilter(None), Command('new'))
async def cmd_new(message: Message, state: FSMContext):
    # await message.answer(text=f'Выбе {message.date}')
    if not await volunteer_table.is_volounteer(message.from_user.id):
        await message.answer(text='Только волонтёры могут добавлять питомцев')
        return
    uuid = await pet_table.add_new_pet(message.from_user.id)
    data = await state.get_data()
    await state.update_data(uuid=uuid)
    await message.answer(text='Выберите тип питомца',
                         reply_markup=get_pet_kb(uuid=uuid))
    await state.set_state(AddPet.choosing_pet_type)


@router.callback_query(AddPet.choosing_pet_type, PetTypeCallback.filter())
async def choose_pet_gender(query: CallbackQuery, state: FSMContext, callback_data: PetTypeCallback):
    try:    await query.message.delete()
    except:  ...
    if callback_data.pet_type == 'dog':
        smile = "🐕"
    else:
        smile = "🐈"
    # await query.message.answer(text=f'Введите описание питомца {smile}')
    # await state.set_state(AddPet.choosing_pet_promt)
    await query.message.answer(text=f'Укажите пол питомца {smile}', reply_markup=get_choosing_gender_kb())
    await state.set_state(AddPet.choosing_pet_gender)
    await pet_table.update_pet_type(callback_data.pet_type, callback_data.uuid)


@router.message(AddPet.choosing_pet_type)
async def choose_pet_gender_stop(message: Message, state: FSMContext):
    await message.answer(text='Вы не нажали на кнопку, заполнение карточки питомца остановлено. Введите последнюю команду повторно')
    data = await state.get_data()
    uuid = data['uuid']
    await pet_table.delete_pet(uuid)
    await state.set_state(None)


@router.callback_query(AddPet.choosing_pet_gender, PetGenderCallback.filter())
async def choose_pet_gender(query: CallbackQuery, state: FSMContext, callback_data: PetGenderCallback):
    try:    await query.message.delete()
    except:  ...
    data = await state.get_data()
    uuid = data['uuid']
    await query.message.answer(text=f'Какая кличка у питомца?',
                               reply_markup=get_skip_button(PetNameCallback,
                                                            pet_name='пока нет имени'))
    await state.set_state(AddPet.choosing_pet_name)
    await pet_table.update_pet_column(uuid, gender=callback_data.pet_gender)
    

@router.message(AddPet.choosing_pet_gender)
async def choose_pet_gender_stop(message: Message, state: FSMContext):
    await message.answer(text='Вы не нажали на кнопку, заполнение карточки питомца остановлено. Введите последнюю команду повторно')
    data = await state.get_data()
    uuid = data['uuid']
    await pet_table.delete_pet(uuid)
    await state.set_state(None)


@router.callback_query(AddPet.choosing_pet_name, PetNameCallback.filter())
async def choose_pet_gender_callback(query: CallbackQuery, state: FSMContext, callback_data: PetNameCallback):
    await state.set_state(AddPet.choosing_pet_age)
    await choose_pet_name(query.message, state, from_callback=True)
    try:    await query.message.delete()
    except:  ...



    
@router.message(AddPet.choosing_pet_name, F.text)
async def choose_pet_name(message: Message, state: FSMContext, from_callback: bool = False):
    # print('HERE!')
    
    data = await state.get_data()
    uuid = data['uuid']
    if message.text.startswith('/'):
        await message.answer('Заполнение анкеты остановлено. Отправьте последнюю команду заново.')
        await pet_table.delete_pet(uuid)
        await state.set_state(None)
        return

    await message.answer(text=f'Укажите возраст питомца \nНапример, 3 месяца, 2.5 года')

    await state.set_state(AddPet.choosing_pet_age)
    if not from_callback:
        await pet_table.update_pet_column(uuid, name=message.text)




@router.message(AddPet.choosing_pet_age, F.text)
async def choose_pet_age(message: Message, state: FSMContext):
    # print('HERE!')
    data = await state.get_data()
    uuid = data['uuid']
    if message.text.startswith('/'):
        await message.answer('Заполнение анкеты остановлено. Отправьте последнюю команду заново.')
        await pet_table.delete_pet(uuid)
        await state.set_state(None)
        return
    
    await message.answer(text=f'Укажите вес питомца \nНапример, 2 кг')

    await state.set_state(AddPet.choosing_pet_weight)
    await pet_table.update_pet_column(uuid, age=message.text)




@router.message(AddPet.choosing_pet_weight, F.text)
async def choose_pet_weight(message: Message, state: FSMContext):
    # print('HERE!')
    data = await state.get_data()
    uuid = data['uuid']
    if message.text.startswith('/'):
        await message.answer('Заполнение анкеты остановлено. Отправьте последнюю команду заново.')
        await pet_table.delete_pet(uuid)
        await state.set_state(None)
        return
    await message.answer(text=f'Питомец чипирован?', reply_markup=get_choosing_chip_kb())

    await state.set_state(AddPet.choosing_pet_chip)
    await pet_table.update_pet_column(uuid, weight=message.text)


#######
@router.callback_query(AddPet.choosing_pet_chip, PetChipCallback.filter())
async def choose_pet_chip(query: CallbackQuery, state: FSMContext, callback_data: PetChipCallback):
    try:    await query.message.delete()
    except:  ...
    data = await state.get_data()
    uuid = data['uuid']
    await query.message.answer(text=f'Укажите информацию о прививках',
                               reply_markup=get_skip_button(PetVaccinationsCallback,
                                                            pet_vaccinations=''))
    await state.set_state(AddPet.choosing_pet_vaccinations)
    await pet_table.update_pet_column(uuid, has_chip=callback_data.pet_chip)


@router.message(AddPet.choosing_pet_chip)
async def choose_pet_gender_stop(message: Message, state: FSMContext):
    await message.answer(text='Вы не нажали на кнопку, заполнение карточки питомца остановлено. Введите последнюю команду повторно')
    data = await state.get_data()
    uuid = data['uuid']
    await pet_table.delete_pet(uuid)
    await state.set_state(None)


@router.callback_query(AddPet.choosing_pet_vaccinations, PetVaccinationsCallback.filter())
async def choose_pet_vaccinations_callback(query: CallbackQuery, state: FSMContext, callback_data: PetVaccinationsCallback):
    await state.set_state(AddPet.choosing_pet_castration)
    await choose_pet_vaccinations(query.message, state, from_callback=True)
    try:    await query.message.delete()
    except:  ...
    await query.answer()


@router.message(AddPet.choosing_pet_vaccinations, F.text)
async def choose_pet_vaccinations(message: Message, state: FSMContext, from_callback: bool = False):
    data = await state.get_data()
    uuid = data['uuid']
    if message.text.startswith('/'):
        await message.answer('Заполнение анкеты остановлено. Отправьте последнюю команду заново.')
        await pet_table.delete_pet(uuid)
        await state.set_state(None)
        return
    
    await message.answer(text=f'Кастрация / стерилизация', reply_markup=get_choosing_castration_kb())

    await state.set_state(AddPet.choosing_pet_castration)
    if from_callback:
        return
    await pet_table.update_pet_column(uuid, vaccinations=message.text)



@router.callback_query(AddPet.choosing_pet_castration, PetCastrationCallback.filter())
async def choose_pet_chip(query: CallbackQuery, state: FSMContext, callback_data: PetCastrationCallback):
    try:    await query.message.delete()
    except:  ...
    data = await state.get_data()
    uuid = data['uuid']
    await query.message.answer(text=f'Укажите информацию об особом уходе, если необходимо',
                               reply_markup=get_skip_button(PetSpecialCareCallback, default_text='Не требуется',
                                                            pet_special_care='Не требуется'))
    await state.set_state(AddPet.choosing_pet_special_care)
    await pet_table.update_pet_column(uuid, castration=callback_data.pet_castration)


@router.message(AddPet.choosing_pet_castration)
async def choose_pet_gender_stop(message: Message, state: FSMContext):
    await message.answer(text='Вы не нажали на кнопку, заполнение карточки питомца остановлено. Введите последнюю команду повторно')
    data = await state.get_data()
    uuid = data['uuid']
    if message.text.startswith('/'):
        await message.answer('Заполнение анкеты остановлено. Отправьте последнюю команду заново.')
        await pet_table.delete_pet(uuid)
        await state.set_state(None)
        return
    await pet_table.delete_pet(uuid)
    await state.set_state(None)



@router.callback_query(AddPet.choosing_pet_special_care, PetSpecialCareCallback.filter())
async def choose_pet_special_care_callback(query: CallbackQuery, state: FSMContext, callback_data: PetSpecialCareCallback):
    await state.set_state(AddPet.choosing_pet_city)
    await choose_pet_special_care(query.message, state, from_callback=True, user_id=query.from_user.id)
    try:    await query.message.delete()
    except:  ...
    await query.answer()


@router.message(AddPet.choosing_pet_special_care, F.text)
async def choose_pet_special_care(message: Message, state: FSMContext, from_callback: bool = False, user_id: int = None):    
    if not from_callback:
        user_id = message.from_user.id

    default_city = await volunteer_table.get_volunteer_city(user_id)
    print(f'city = {default_city}')
    print('\n' * 5)
    await message.answer(text='Введите город, в котором находится питомец',
                         reply_markup=get_choosing_default_city_kb(default_city=default_city))
    
    # await message.answer(text=f'Отправьте фото питомца')
    #await state.set_state(AddPet.choosing_pet_photo)
    await state.set_state(AddPet.choosing_pet_city)
    if from_callback:
        return
    data = await state.get_data()
    uuid = data['uuid']
    await pet_table.update_pet_column(uuid, special_care=message.text)


@router.callback_query(AddPet.choosing_pet_city, PetCityCallback.filter())
async def choose_pet_city_callback(query: CallbackQuery, state: FSMContext, callback_data: PetCityCallback):
    # print('HEREERREREREREREREEEEEEEEEEEEEEEEEEEEEE!!!')
    try:    await query.message.delete()
    except:  ...
    await state.set_state(AddPet.choosing_pet_photo)
    await choose_pet_city(query.message, state, from_callback=True, default_city=callback_data.pet_city)
    # print(f'ДОЛЖНО БЫТЬ УДАЛЕНИЕ КНОПКИ \n\n\n\n\n\n')
    
    # await query.answer()


@router.message(AddPet.choosing_pet_city, F.text)
async def choose_pet_city(message: Message, state: FSMContext, from_callback: bool = False, default_city: str = None):
    data = await state.get_data()
    uuid = data['uuid']

    if from_callback:
        corrected_city = default_city
    else: 
        corrected_city = get_corrected_city(message.text)

    if len(corrected_city) == 0:
        await message.answer(text='Некорректное название города')
        return
    
    await pet_table.update_pet_column(uuid, city=corrected_city)
    await message.answer(text=f'Отправьте фото питомца')
    await state.set_state(AddPet.choosing_pet_photo)


################################
# @router.callback_query(AddPet.choosing_pet_type, PetTypeCallback.filter())
# async def choose_pet_type(query: CallbackQuery, state: FSMContext, callback_data: PetTypeCallback):
#     try:    await query.message.delete()
#     except:  ...
#     if callback_data.pet_type == 'dog':
#         smile = "🐕"
#     else:
#         smile = "🐈"
#     # await query.message.answer(text=f'Введите описание питомца {smile}')
#     # await state.set_state(AddPet.choosing_pet_promt)
#     await query.message.answer(text=f'Отправьте фото питомца {smile}')
#     await state.set_state(AddPet.choosing_pet_photo)
#     await pet_table.update_pet_type(callback_data.pet_type, callback_data.uuid)


@router.message(AddPet.choosing_pet_promt, F.text)
async def make_prompt(message: Message, state: FSMContext):
    if message.text.startswith('/'):
        await state.set_state(None)
        await message.answer(text='Создание анкеты завершено, введите команду заново')
        return 

    prompt = message.text
    data = await state.get_data()
    uuid = data['uuid']
    await pet_table.update_pet_prompt(prompt, uuid)

    # pet_type = await pet_table.get_pet_type(uuid)
    pet = await pet_table.get_info_from_pet(uuid)
    sent_msg = await message.answer(text='Создаем описание...✏️')
    description = await make_description(pet) #message.text #+ 'description'

    await pet_table.update_pet_description(description, uuid)
    await message.answer(text=f'Описание питомца: \n{description}',
                         reply_markup=get_agree_description_kb())
    await sent_msg.delete()


@router.message(AddPet.choosing_pet_photo, F.photo)
async def pick_photo(message: Message, state: FSMContext):
    photos = message.photo
    for photo in photos:
        photo_id = photo.file_id
        break
    data = await state.get_data()
    uuid = data['uuid']
    await pet_table.update_pet_photo(photo_id, uuid)
    await message.answer(text='Отправьте описание питомца')

    await state.set_state(AddPet.choosing_pet_promt)
    # await state.set_state(None)
    # await pet_table.update_available_pet(available=True, uuid=uuid)
    # pet = await pet_table.get_info_from_pet(uuid)
    # text = "<b>Карточка питомца:</b> \n" + pet.description
    # await message.answer_photo(pet.pet_photo_id, caption=text)


@router.message(AddPet.choosing_pet_photo)
async def choose_pet_gender_stop(message: Message, state: FSMContext):
    await message.answer(text='Вы не отпрвили фото питомца, заполнение карточки питомца остановлено. Введите последнюю команду повторно')
    data = await state.get_data()
    uuid = data['uuid']
    await pet_table.delete_pet(uuid)
    await state.set_state(None)


@router.callback_query(AddPet.choosing_pet_promt, AgreeDescriptionCallback.filter())
async def agree_prompt(query: CallbackQuery, state: FSMContext, callback_data: AgreeDescriptionCallback):
    data = await state.get_data()
    uuid = data['uuid']
    if callback_data.agree:
        try:    await query.message.delete()
        except:  ...
        # await query.message.answer(text='Отправьте фото питомца')
        # await state.set_state(AddPet.choosing_pet_photo)
        
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
        # prompt = await pet_table.get_prompt(uuid)
        # pet_type = await pet_table.get_pet_type(uuid)
        sent_msg = await query.message.answer(text='Создаем описание...✏️')
        new_description = await make_description(pet) #message.text #+ 'description'

        await pet_table.update_pet_description(new_description, uuid)
        
        try:    await query.message.delete()
        except:  ...

        await query.message.answer(text=f'Описание питомца: \n{new_description}',
                         reply_markup=get_agree_description_kb())

        await sent_msg.delete()