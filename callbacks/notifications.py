from aiogram.filters.callback_data import CallbackData
from uuid import UUID


class ShowPetsCallback(CallbackData, prefix='show_pets'):
    city: str


class OffNotificationCallback(CallbackData, prefix='off_notification'):
    ...

class AdminRepostPetCallback(CallbackData, prefix='admin_reposted'):
    delete_msg: bool = False