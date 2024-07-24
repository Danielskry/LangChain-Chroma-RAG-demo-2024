
from os import environ

from dotenv import load_dotenv

load_dotenv()

def get_environment() -> str:
    """ Gets application environment """
    return environ.get('APP_ENV') or 'development'
