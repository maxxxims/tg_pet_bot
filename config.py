from dotenv import load_dotenv
import os

OWNERS_ID = [683099207] #, 1737030496]

DELAY_BETWEEN_NOTIFICATIONS_IN_SECONDS = 0.1

DEFAULT_NOTIFICATION_TO_ADMIN = "Появился новый питомец!"


MSG_AFTER_ADMIN_REGISTRATION = """Поздравляем, регистрация завершена!
Теперь вы будете получать информацию о питомцах в вашем городе.
Чтобы посмотреть список добавленных животных, введите команду /pets"""

MSG_AFTER_REGISTRATION = """Чтобы добавить питомца, введите команду /new
Чтобы посмотреть список добавленных животных, введите команду /pets"""


MSG_PET_DESCRIPTION = """Выберите необходимый пункт"""

def get_owner_tg_id():
    load_dotenv()
    return int(os.getenv('OWNER_ID'))

def load_bot_token():
    #return '6937977238:AAGZWXGSeheZy1eXfAJVC9mUvhl5fk7D358'
    load_dotenv()
    return os.getenv("BOT_TOKEN_PROD")


def load_db_url():
    load_dotenv()
    return os.getenv("DB_URL_PROD")


def load_openai_token():
    load_dotenv()
    return os.getenv("OPENAI_TOKEN")