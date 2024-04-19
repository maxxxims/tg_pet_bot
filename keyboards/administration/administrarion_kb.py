from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardMarkup
from callbacks import *
from uuid import UUID


def get_kb_choose_city_to_admin() -> InlineKeyboardMarkup:
    """
        🐕 🐈
    """
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Любой', callback_data=AdministrationChooseAnyCityCallback().pack()),
            ]
        ]
    )

    return kb


def get_kb_navigation_for_administration(city: str, pet_uuid: UUID, offset: int  = 0):
    
    if offset == 0:
        kb_list = [
            [
                InlineKeyboardButton(text='❌ Закрыть', callback_data=AdministrationStopNavigationCallback().pack()),
                InlineKeyboardButton(text='➡️', callback_data=AdministrationNavigationButtonCallback(city=city, offset=offset, ofsset_delta=1).pack()),
            ],
            [
                InlineKeyboardButton(text='🗑️ Удалить карточку', callback_data=AdminDeleteVolunteerCardCallback(uuid=pet_uuid).pack())
            ]]
    else:
        kb_list = [
            [
                InlineKeyboardButton(text='⬅️', callback_data=AdministrationNavigationButtonCallback(city=city, offset=offset, ofsset_delta=-1).pack()),
                InlineKeyboardButton(text='❌ Закрыть', callback_data=AdministrationStopNavigationCallback().pack()),
                InlineKeyboardButton(text='➡️', callback_data=AdministrationNavigationButtonCallback(city=city, offset=offset, ofsset_delta=1).pack()),
            ],
            [
                InlineKeyboardButton(text='🗑️ Удалить карточку', callback_data=AdminDeleteVolunteerCardCallback(uuid=pet_uuid).pack())
            ]]

    
    kb = InlineKeyboardMarkup(inline_keyboard=kb_list)

    return kb