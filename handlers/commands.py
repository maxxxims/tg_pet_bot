from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ContentType
from keyboards import get_pet_navigation_kb
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext



router = Router()


MSG = "Список доступных команд: \n/dog - поиск собаки\n/cat - поиск кошки\n/new - добавить питомца"


@router.message(StateFilter(None), Command('start'))
async def cmd_dog(message: Message, state: FSMContext):
    await message.answer(text=MSG)


@router.message(StateFilter(None), Command('info'))
async def cmd_dog(message: Message, state: FSMContext):
    await message.answer(text=MSG)