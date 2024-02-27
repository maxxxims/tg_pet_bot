from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardMarkup
from collections import defaultdict
import emoji
# from callbacks import PetTypeCallback, AgreeDescriptionCallback, PreviousButtonCallback, NextButtonCallback, \
#     StopNavigationCallback, AddFavouriteCallback, NavigationButtonCallback
from callbacks import *
from uuid import UUID
from fsm import AddPet


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
            ],
            [
                InlineKeyboardButton(text='✍🏼 Ввести своё описание', callback_data=WriteOwnDescriptionCallback().pack()),
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
            ],
            # [
            #     InlineKeyboardButton(text='⬅️ Назад', callback_data=SkipRegistrationStageCallback(
            #         new_stage='choosing_pet_type'
            #     ).pack()),
            # ]
        ]
    )

    return choose_gender_kb


def get_choosing_castration_kb():
    choose_chip_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Есть',  callback_data=PetCastrationCallback(pet_castration=True).pack()),
                InlineKeyboardButton(text='Пропустить', callback_data=SkipRegistrationStageCallback(
                    new_stage='choose_pet_special_care'
                ).pack()),
                InlineKeyboardButton(text='Нет', callback_data=PetCastrationCallback(pet_castration=False).pack()),
            ],
            [
                InlineKeyboardButton(text='⬅️ Назад', callback_data=SkipRegistrationStageCallback(
                    new_stage='choose_pet_vaccinations'
                ).pack()),
            ]
        ]
    )

    return choose_chip_kb


def get_choosing_chip_kb():
    choose_chip_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Да',  callback_data=PetChipCallback(pet_chip=True).pack()),
                InlineKeyboardButton(text='Пропустить', callback_data=SkipRegistrationStageCallback(
                    new_stage='choose_pet_castration').pack()),
                InlineKeyboardButton(text='Нет', callback_data=PetChipCallback(pet_chip=False).pack()),
            ],
            [
                InlineKeyboardButton(text='⬅️ Назад', callback_data=SkipRegistrationStageCallback(
                    new_stage='choose_pet_weight'
                ).pack()),
            ]
        ]
    )

    return choose_chip_kb


def get_skip_button(callback: CallbackData, new_stage: str,
                    default_text: str = 'Пропустить', **kwargs):
    skip_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=default_text, callback_data=callback(skip=True, **kwargs).pack())
            ],
            [
                InlineKeyboardButton(text='⬅️ Назад', callback_data=SkipRegistrationStageCallback(new_stage=new_stage).pack())
            ]
        ]
    )

    return skip_kb



def get_skip_button_and_back(back_stage: str, foward_stage: str,  foward_text: str = 'Пропустить'):
    skip_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=foward_text, callback_data=SkipRegistrationStageCallback(new_stage=foward_stage).pack())
            ],
            [
                InlineKeyboardButton(text='⬅️ Назад', callback_data=SkipRegistrationStageCallback(new_stage=back_stage).pack())
            ]
        ]
    )

    return skip_kb



def get_kb_for_photo():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='⬅️ Назад', callback_data=SkipRegistrationStageCallback(new_stage='choose_pet_city').pack())
            ]
        ]
    )

    return kb


def get_kb_for_description():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='⬅️ Назад', callback_data=SkipRegistrationStageCallback(new_stage='choose_pet_photo').pack())
            ]
        ]
    )

    return kb