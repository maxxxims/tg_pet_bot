from aiogram.filters.callback_data import CallbackData



class RegistrationProfileTypeCallback(CallbackData, prefix='registration_profile_type'):
    profile_type: str