from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


class AddPet(StatesGroup):
    choosing_pet_type = State()
    choosing_pet_promt = State()
    choosing_pet_photo = State()
