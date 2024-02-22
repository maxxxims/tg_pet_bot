from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


class AddPet(StatesGroup):
    choosing_pet_type = State()

    choosing_pet_gender = State()
    choosing_pet_name = State()
    choosing_pet_age = State()
    choosing_pet_weight = State()

    choosing_pet_chip = State()
    choosing_pet_vaccinations = State()
    choosing_pet_castration = State()
    choosing_pet_special_care = State()
    
    choosing_pet_city = State()

    choosing_pet_promt = State()
    writing_own_description = State()
    choosing_pet_photo = State()



class AdminRegistration(StatesGroup):
    writing_channel_name = State()
    writing_city = State()
    