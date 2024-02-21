from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardMarkup
from collections import defaultdict
import emoji
from callbacks import *
from uuid import UUID


def get_show_notification_kb(city: str):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Посмотреть доступных питомцев', callback_data=ShowPetsCallback(city=city).pack())
            ],
            [
                InlineKeyboardButton(text='Отключить уведомления', callback_data=OffNotificationCallback().pack()),
            ]
        ]
    )
    return kb



def get_kb_for_notification(send_to: str, offset: int) -> InlineKeyboardMarkup:
    if offset == 0:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='❌ Закрыть', callback_data=StopNavigationCallback().pack()),
                    InlineKeyboardButton(text='➡️', callback_data=NavigationButtonCallback(send_to=send_to, offset=offset, ofsset_delta=1).pack()),
                ],
                [
                    InlineKeyboardButton(text='✔️Я опубликовал в своём канале', callback_data=AdminRepostPetCallback().pack()),
                ]
            ]
        )
    
    else:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='⬅️', callback_data=NavigationButtonCallback(send_to=send_to, offset=offset, ofsset_delta=-1).pack()),
                    InlineKeyboardButton(text='❌ Закрыть', callback_data=StopNavigationCallback().pack()),
                    InlineKeyboardButton(text='➡️', callback_data=NavigationButtonCallback(send_to=send_to, offset=offset, ofsset_delta=+1).pack()),
                ],
                [
                    InlineKeyboardButton(text='✔️Я опубликовал в своём канале', callback_data=AdminRepostPetCallback().pack()),
                ]
            ]
        )
    


def get_notification_kb_for_admin() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='✔️Я опубликовал в своём канале', callback_data=AdminRepostPetCallback(delete_msg=True).pack()),
            ]
        ]
    )
