from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardMarkup
from collections import defaultdict
import emoji
from callbacks import *
from uuid import UUID


def get_profile_type_kb():
    choose_profile_type_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Волонтёр', callback_data=RegistrationProfileTypeCallback(profile_type='volunteer').pack())
            ],
            [
                InlineKeyboardButton(text='Администратор канала', callback_data=RegistrationProfileTypeCallback(profile_type='admin').pack()),
            ]
        ]
    )
    return choose_profile_type_kb



def get_choosing_default_city_kb(default_city: str):
    choose_city_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=default_city, callback_data=PetCityCallback(pet_city=default_city).pack())
            ]
        ]
    )
    return choose_city_kb