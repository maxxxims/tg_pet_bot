
from aiogram.types import CallbackQuery
from callbacks import NavigationButtonCallback
from .make_description import make_pet_description 
from keyboards import get_pet_navigation_kb
from models import Pet
from aiogram.types import InlineKeyboardMarkup


async def navigation_button_function(
        query: CallbackQuery,
        callback_data: NavigationButtonCallback,
        keyboard: InlineKeyboardMarkup,
        pet: Pet, new_offset: int = 0, show_alert: bool = True
        ):
    
    if pet is None:
        #await query.message.answer(text='Больше нет доступных питомцев')
        await query.answer(text='Больше нет доступных питомцев', show_alert=show_alert)
        return
    description = make_pet_description(pet)
    try:    await query.message.delete()
    except:  ...
    await query.message.answer_photo(
        photo=pet.pet_photo_id,
        caption=description,
        parse_mode="HTML",
        reply_markup=keyboard
    )
    await query.answer()