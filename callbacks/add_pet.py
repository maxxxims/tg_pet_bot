from aiogram.filters.callback_data import CallbackData
from uuid import UUID


class PetTypeCallback(CallbackData, prefix='pet_type'):
    pet_type: str
    uuid: UUID

class AgreeDescriptionCallback(CallbackData, prefix='description'):
    agree: bool


class PreviousButtonCallback(CallbackData, prefix='previous'):
    pet_type: str
    offset: int


class NextButtonCallback(CallbackData, prefix='next'):
    pet_type: str
    offset: int


class NavigationButtonCallback(CallbackData, prefix='navigation'):
    pet_type: str
    offset: int
    ofsset_delta: int

class StopNavigationCallback(CallbackData, prefix='stop'):
    ...


class AddFavouriteCallback(CallbackData, prefix='favourite'):
    uuid: UUID