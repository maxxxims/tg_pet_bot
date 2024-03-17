from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardMarkup
from collections import defaultdict
import emoji
from callbacks import ShowAdminNotificationCallback, ShowVolunteerPetsCallback, StopNavigationCallback, \
    NavigationButtonCallback, DeleteVolunteerPetCallback, AdministrationShowPetsCallback
from uuid import UUID


def get_choosing_type_of_my_pets():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Показать ваших добавленных питомцев', callback_data=ShowVolunteerPetsCallback().pack())
            ],
            [
                InlineKeyboardButton(text='Показать уведомления о новых питомцах', callback_data=ShowAdminNotificationCallback().pack()),
            ],
            [
                InlineKeyboardButton(text='Показать всех питомцев', callback_data=AdministrationShowPetsCallback().pack())
            ]
        ]
    )
    return kb




def get_navigation_kb_for_volunteer(uuid: UUID, offset: int) -> InlineKeyboardMarkup:
    if offset == 0:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='❌ Закрыть', callback_data=StopNavigationCallback().pack()),
                    InlineKeyboardButton(text='➡️', callback_data=NavigationButtonCallback(send_to='volunteer', offset=offset, ofsset_delta=1).pack()),
                ],
                [
                    InlineKeyboardButton(text='🗑️ Удалить карточку', callback_data=DeleteVolunteerPetCallback(uuid=uuid, current_offset=offset).pack())
                ]
            ]
        )
    
    else:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='⬅️', callback_data=NavigationButtonCallback(send_to='volunteer', offset=offset, ofsset_delta=-1).pack()),
                    InlineKeyboardButton(text='❌ Закрыть', callback_data=StopNavigationCallback().pack()),
                    InlineKeyboardButton(text='➡️', callback_data=NavigationButtonCallback(send_to='volunteer', offset=offset, ofsset_delta=+1).pack()),
                ],
                [
                    InlineKeyboardButton(text='🗑️ Удалить карточку', callback_data=DeleteVolunteerPetCallback(uuid=uuid, current_offset=offset).pack())
                ]
            ]
        )