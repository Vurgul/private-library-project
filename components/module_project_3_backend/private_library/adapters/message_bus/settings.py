import os
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    user = os.getenv('RABBITMQ_USER', 'user')
    password = os.getenv('RABBITMQ_PASSWORD', 'password')
    host = os.getenv('RABBITMQ_HOST', 'localhost')
    port = os.getenv('RABBITMQ_PORT', '5432')

    BROKER_URL: Optional[str] = f'amqp://{user}:{password}@{host}:{port}'

    LOGGING_LEVEL: str = 'INFO'

    @property
    def LOGGING_CONFIG(self):
        return {
            'loggers': {
                'kombu': {
                    'handlers': ['default'],
                    'level': self.LOGGING_LEVEL,
                    'propagate': False
                }
            }
        }
