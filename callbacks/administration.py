from aiogram.filters.callback_data import CallbackData
from uuid import UUID


class AdministrationShowPetsCallback(CallbackData, prefix='show'):   ...

class AdministrationChooseAnyCityCallback(CallbackData, prefix='choose_any_city'):   ...

class AdministrationStopNavigationCallback(CallbackData, prefix='stop_navigation_administration'):   ...

class AdministrationNavigationButtonCallback(CallbackData, prefix='navigation_administration'):
    offset: int
    city: str
    ofsset_delta: int


class AdminDeleteVolunteerCardCallback(CallbackData, prefix='dvcb'):
    uuid: UUID
    

class AgreementDeleteCallbakc(CallbackData, prefix='del'):
    pet_uuid: UUID
    msg_id: int
    
class CloseDeleteCallback(CallbackData, prefix='close'):    ...