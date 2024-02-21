from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


class VolunteerRegistration(StatesGroup):
    start_registration = State()
    writing_name = State()
    writing_surname = State()
    writing_phone = State()
    writing_city = State()
