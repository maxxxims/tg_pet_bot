from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


class AdminShowPets(StatesGroup):
    choosing_city = State()