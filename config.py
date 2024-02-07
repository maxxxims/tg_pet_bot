from dotenv import load_dotenv
import os


def load_bot_token():
    load_dotenv()
    return os.getenv("BOT_TOKEN")


def load_db_url():
    load_dotenv()
    return os.getenv("DB_URL")


def load_openai_token():
    load_dotenv()
    return os.getenv("OPENAI_TOKEN")