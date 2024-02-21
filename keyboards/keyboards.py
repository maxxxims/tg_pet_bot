from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardMarkup
from collections import defaultdict
import emoji
# from callbacks import PetTypeCallback, AgreeDescriptionCallback, PreviousButtonCallback, NextButtonCallback, \
#     StopNavigationCallback, AddFavouriteCallback, NavigationButtonCallback
from callbacks import *
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
    

def get_choosing_gender_kb():
    choose_gender_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Мальчик', callback_data=PetGenderCallback(pet_gender='мальчик').pack()),
                InlineKeyboardButton(text='Девочка', callback_data=PetGenderCallback(pet_gender='девочка').pack()),
            ]
        ]
    )

    return choose_gender_kb


def get_choosing_castration_kb():
    choose_chip_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Есть',  callback_data=PetCastrationCallback(pet_castration=True).pack()),
                InlineKeyboardButton(text='Нет', callback_data=PetCastrationCallback(pet_castration=False).pack()),
            ]
        ]
    )

    return choose_chip_kb


def get_choosing_chip_kb():
    choose_chip_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Да',  callback_data=PetChipCallback(pet_chip=True).pack()),
                InlineKeyboardButton(text='Нет', callback_data=PetChipCallback(pet_chip=False).pack()),
            ]
        ]
    )

    return choose_chip_kb


def get_skip_button(callback: CallbackData, default_text: str = 'Пропустить', **kwargs):
    skip_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=default_text, callback_data=callback(skip=True, **kwargs).pack())
            ]
        ]
    )

    return skip_kb