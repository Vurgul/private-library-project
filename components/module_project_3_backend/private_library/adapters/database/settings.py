import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    user = os.getenv('USER', 'user')
    password = os.getenv('PASSWORD', 'password')
    host = os.getenv('HOST', 'localhost')
    port = os.getenv('PORT', '5432')
    database = os.getenv('DATABASE', 'test')

    DB_URL = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

    LOGGING_LEVEL: str = 'INFO'
    SA_LOGS: bool = False

    @property
    def LOGGING_CONFIG(self):
        config = {
            'loggers': {
                'alembic': {
                    'handlers': ['default'],
                    'level': self.LOGGING_LEVEL,
                    'propagate': False
                }
            }
        }

        if self.SA_LOGS:
            config['loggers']['sqlalchemy'] = {
                'handlers': ['default'],
                'level': self.LOGGING_LEVEL,
                'propagate': False
            }

        return config
