from models import Pet
from aiogram import html, Bot


def get_pet_gender(pet: Pet):   return '\n' + f'<b>Пол:</b> {pet.gender}'
def get_pet_name(pet: Pet):     return '\n' + f'<b>Кличка:</b> {pet.name if pet.name is not None else "нет имени"}'
def get_pet_age(pet: Pet):      
    if pet.age is None:
        return ''
    return '\n' + f'<b>Возраст:</b> {pet.age}'
def get_pet_weight(pet: Pet):   
    if pet.weight is None:
        return ''
    return '\n' + f'<b>Вес:</b> {pet.weight}'

def get_pet_city(pet: Pet):     return '\n' + f'<b>Город:</b> {pet.city}'
def get_pet_vaccinations(pet: Pet):     return '\n' + f'<b>Вакцинация:</b> {pet.vaccinations if pet.vaccinations is not None else "нет информации"}'
def get_pet_special_care(pet: Pet):     return '\n' + f'<b>Особый уход:</b> {pet.special_care if pet.special_care is not None else "не требуется"}'

def get_pet_chip(pet: Pet):
    if pet.has_chip is not None:
        has_chip = '\n' + f'<b>Чипирован:</b> {"да" if pet.has_chip else "нет"}'
    else:
        has_chip = ''
    return has_chip


def get_pet_castration(pet: Pet): 
    if pet.castration is not None:
        castration = '\n' + f'<b>Кастрация:</b> {"да" if pet.castration else "нет"}'
    else:
        castration = ''
    return castration


async def get_owner(pet: Pet, bot: Bot):
    try:
        user = await bot.get_chat(pet.volunteer_tg_id)
        return '<b>Владелец: </b>' + f'@{user.username}'
    except:
        return '<b>Владелец: </b>' + f'<a href="tg://user?id={pet.volunteer_tg_id}">{pet.volunteer.nick}</a>'
    #return '<b>Владелец: </b>' + html.link(pet.volunteer.nick, link=f'tg://openmessage?user_id={pet.volunteer_tg_id}')
    #return '<b>Владелец: </b>' + f"<a href=tg://user?id={pet.volunteer_tg_id}>{pet.volunteer.name}</a>"
    #if pet.volunteer.username is None:
    #    return '<b>Владелец: </b>' + f'<a href="tg://user?id={pet.volunteer_tg_id}">{pet.volunteer.nick}</a>'
    #else:
    #    return '<b>Владелец: </b>' + f'@{pet.volunteer.username}'


async def get_onwer_to_admin(pet: Pet, bot: Bot):
    try:
        user = await bot.get_chat(pet.volunteer_tg_id)
        return '<b>Владелец: </b>' + f'@{user.username}'
    except:
        return '<b>Владелец: </b>' + f'<a href="tg://user?id={pet.volunteer_tg_id}">{pet.nick}</a>'
    return '<b>Владелец: </b>' + html.link(pet.nick, link=f'tg://user?id={pet.volunteer_tg_id}')
    if pet.username is None:
        return '<b>Владелец: </b>' + f'<a href="tg://user?id={pet.volunteer_tg_id}">{pet.nick}</a>'
    else:
        return '<b>Владелец: </b>' + f'@{pet.username}'


def additional_info():
    return f'\nРепост приветствуется 🙏🏻'


async def make_pet_description(pet: Pet, bot: Bot, to_admin: bool = False, additional: bool = True):
    #user_name = f'[{pet.volunteer.nick}](tg://user?id={str({pet.volunteer_tg_id})})'
    #user_name = f'[{pet.owner_nick}](tg://user?id={str({pet.owner_id})})'
    gender = get_pet_gender(pet)
    name = get_pet_name(pet)
    age = get_pet_age(pet)
    weight = get_pet_weight(pet)
    has_chip = get_pet_chip(pet)
    vaccinations = get_pet_vaccinations(pet)
    castration = get_pet_castration(pet)
    special_care = get_pet_special_care(pet)
    city = get_pet_city(pet)
    if to_admin:
        owner = await get_onwer_to_admin(pet, bot)
    else:
        owner = await get_owner(pet, bot)

    text = pet.description + '\n' + ' \n' + '<u><b>Дополнительная информация:</b></u>'
    
    text = text + name + gender + age + weight + has_chip + castration + vaccinations + special_care + city

    # text = text + '\n' + '<b>Владелец:<b> ' + f'[{pet.volunteer.nick}](tg://user?id={str(pet.volunteer_tg_id)})'

    text = text + '\n' + owner
    if additional:  text += additional_info()
    
    return text
