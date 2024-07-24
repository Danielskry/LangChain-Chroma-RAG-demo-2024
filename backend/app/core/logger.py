from logging import Logger, getLogger

from app.config import config as app_config
from app.core.environment import get_environment


def get_logger(name) -> Logger:
    """
    Retrieves a logger instance for name.

    Args:
        name (str): The name to be included in the logger.
    """
    return getLogger(f"{app_config[get_environment()].APP_NAME}.{name}")
