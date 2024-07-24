# Configuration for app environment

from enum import Enum
from os import environ, path
from typing import Final

from app.config.llm_config import LLMConfig, OpenAIConfig
from app.config.embedding_config import EmbeddingConfig, \
    OpenAIEmbeddingConfig

basedir = path.abspath(path.join(path.dirname(__file__), '../../'))

class BaseConfig(object):
    """ Base config class. """

    # FastAPI API app details
    APP_VERSION: Final = "1.0.0"
    APP_NAME: Final = "Chroma RAG demo"
    APP_DESCRIPTION: Final = "A description of the demo"
    
    # LLM Configuration
    LLM: LLMConfig = OpenAIConfig()
    
    # Embedding configuration
    EMBEDDINGS: EmbeddingConfig = OpenAIEmbeddingConfig()

    # Logging
    LOGGING: dict = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '[%(asctime)s] - %(name)s - %(levelname)s - %(message)s',
                'datefmt': '%b %d %Y %H:%M:%S'
            },
            'simple': {
                'format': '%(levelname)s - %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
        },
        'loggers': {
            '': {  # Root logger
                'level': 'DEBUG',
                'handlers': ['console'],
            },
        },
    }

    CORS_ORIGINS: list = ['*']
    ALLOWED_METHODS: list = ['*']
    ALLOWED_HEADERS: list = ['*']

class Development(BaseConfig):
    """ Development config. """

    DEBUG = True
    TESTING = False
    ENV = 'dev'

class Testing(BaseConfig):
    """ Testing config. """

    DEBUG = True
    TESTING = True
    ENV = 'testing'

class Production(BaseConfig):
    """ Production config """

    DEBUG = False
    TESTING = False
    ENV = 'production'

config = {
    'development': Development,
    'testing': Testing,
    'production': Production,
}
