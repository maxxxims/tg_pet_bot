from aiogram.filters.callback_data import CallbackData
from uuid import UUID


class SkipButtonCallback(CallbackData, prefix='skip'):
    skip: bool = True


class PetGenderCallback(CallbackData, prefix='pet_gender'):
    pet_gender: str

class PetNameCallback(CallbackData, prefix='pet_name'):
    pet_name: str
    skip: bool = False

class PetAgeCallback(CallbackData, prefix='pet_age'):
    pet_age: str
    skip: bool = False

class PetWeightCallback(CallbackData, prefix='pet_weight'):
    pet_weight: int
    skip: bool = False


class PetChipCallback(CallbackData, prefix='pet_chip'):
    pet_chip: bool
    skip: bool = False


class PetVaccinationsCallback(CallbackData, prefix='pet_vaccinations'):
    pet_vaccinations: str
    skip: bool = False
    



class PetCastrationCallback(CallbackData, prefix='pet_castration'):
    pet_castration: bool
    skip: bool = False
    
class PetSpecialCareCallback(CallbackData, prefix='pet_special_care'):
    pet_special_care: str
    skip: bool = False


class PetCityCallback(CallbackData, prefix='pet_city'):
    pet_city: str


####################
class PetTypeCallback(CallbackData, prefix='pet_type'):
    pet_type: str
    uuid: UUID

class AgreeDescriptionCallback(CallbackData, prefix='description'):
    agree: bool

class WriteOwnDescriptionCallback(CallbackData, prefix='own_description'):
    ...


class PreviousButtonCallback(CallbackData, prefix='previous'):
    pet_type: str
    offset: int


class NextButtonCallback(CallbackData, prefix='next'):
    pet_type: str
    offset: int


class NavigationButtonCallback(CallbackData, prefix='navigation'):
    # pet_type: str
    offset: int
    ofsset_delta: int
    send_to: str = 'admin'

class StopNavigationCallback(CallbackData, prefix='stop'):
    ...


class AddFavouriteCallback(CallbackData, prefix='favourite'):
    uuid: UUID