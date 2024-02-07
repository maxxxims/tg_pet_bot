from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardMarkup
from collections import defaultdict
import emoji
from callbacks import PetTypeCallback, AgreeDescriptionCallback, PreviousButtonCallback, NextButtonCallback, \
    StopNavigationCallback, AddFavouriteCallback, NavigationButtonCallback
from uuid import UUID


def get_pet_kb(uuid: UUID) -> InlineKeyboardMarkup:
    """
        🐕 🐈
    """
    choose_pet_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='🐶', callback_data=PetTypeCallback(pet_type='dog', uuid=uuid).pack()),
                InlineKeyboardButton(text='🐱', callback_data=PetTypeCallback(pet_type='cat', uuid=uuid).pack()),
            ]
        ]
    )

    return choose_pet_kb


def get_agree_description_kb() -> InlineKeyboardMarkup:
    choose_pet_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=emoji.emojize(':left_arrow_curving_right:') + 'Изменить описание ',
                                     callback_data=AgreeDescriptionCallback(agree=False).pack()),
                InlineKeyboardButton(text='✅ Далее',
                                    callback_data=AgreeDescriptionCallback(agree=True).pack()),
            ]
        ]
    )

    return choose_pet_kb



def get_pet_navigation_kb(pet_type: str, offset: int, uuid: UUID) -> InlineKeyboardMarkup:
    if offset == 0:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='❌ ', callback_data=StopNavigationCallback().pack()),
                    InlineKeyboardButton(text='➡️', callback_data=NavigationButtonCallback(pet_type=pet_type, offset=offset, ofsset_delta=1).pack()),
                ],
                [
                    InlineKeyboardButton(text='⭐ В избранное', callback_data=AddFavouriteCallback(uuid=uuid).pack())
                ]
            ]
        )
    
    else:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='⬅️', callback_data=NavigationButtonCallback(pet_type=pet_type, offset=offset, ofsset_delta=-1).pack()),
                    InlineKeyboardButton(text='❌', callback_data=StopNavigationCallback().pack()),
                    InlineKeyboardButton(text='➡️', callback_data=NavigationButtonCallback(pet_type=pet_type, offset=offset, ofsset_delta=+1).pack()),
                ],
                [
                    InlineKeyboardButton(text='⭐ В избранное', callback_data=AddFavouriteCallback(uuid=uuid).pack())
                ]
            ]
        )