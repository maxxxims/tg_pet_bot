from aiogram.filters.callback_data import CallbackData
from uuid import UUID


class MyPetsNextCallback(CallbackData, prefix='previous'):
    pet_type: str
    offset: int


class MyPetsNextCallback(CallbackData, prefix='next'):
    pet_type: str
    offset: int


class MyPetsNavigationButtonCallback(CallbackData, prefix='navigation'):
    pet_type: str
    offset: int
    ofsset_delta: int

class MyPetsCloseCallback(CallbackData, prefix='close'):
    ...


class MyPetsDeleteCallback(CallbackData, prefix='delete'):
    uuid: UUID



class ShowVolunteerPetsCallback(CallbackData, prefix='show_volunteer'):     ...


class ShowAdminNotificationCallback(CallbackData, prefix='show_admin_notification'):     ...


class DeleteVolunteerPetCallback(CallbackData, prefix='delete_volunteer_pet'):
    uuid: UUID
    current_offset: int