# from os import getenv
import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional, AnyStr
from pydantic_settings import BaseSettings


class PydanticConfig(BaseSettings):
    ...
    AS_HOST: Optional[AnyStr] = None
    AS_PORT: Optional[int] = None
    AS_LOG_LEVEL: Optional[int] = None
    AS_LOG_FILE: Optional[AnyStr] = None

    PE_DB_DIALECT: Optional[AnyStr] = None
    PE_DB_USERNAME: Optional[AnyStr] = None
    PE_DB_PASSWORD: Optional[AnyStr] = None
    PE_DB_HOST: Optional[AnyStr] = None
    PE_DB_PORT: Optional[int] = None
    PE_DB_DATABASE: Optional[AnyStr] = None
    PE_DB_ECHO: Optional[bool] = None
    PE_DB_DEFAULT_DATABASE: Optional[AnyStr] = None


class Config:
    def __init__(self, path):
        self.AS_HOST: Optional[AnyStr] = None
        self.AS_PORT: Optional[int] = None
        self.AS_LOG_LEVEL: Optional[int] = None
        self.AS_LOG_FILE: Optional[AnyStr] = None

        self.PE_DB_DIALECT: Optional[AnyStr] = None
        self.PE_DB_NOT_ASYNC_DIALECT: Optional[AnyStr] = None
        self.PE_DB_USERNAME: Optional[AnyStr] = None
        self.PE_DB_PASSWORD: Optional[AnyStr] = None
        self.PE_DB_HOST: Optional[AnyStr] = None
        self.PE_DB_PORT: Optional[int] = None
        self.PE_DB_DATABASE: Optional[AnyStr] = None
        self.PE_DB_ECHO: Optional[bool] = None
        self.load_env(path)

    def load_env(self, path: str):
        load_dotenv(path)
        self.load_as_settings()
        self.load_as_db()

    @staticmethod
    def logging_level_strint_to_int(level: str) -> int:
        level = level.upper()
        string_to_level = {
            'CRITICAL': logging.CRITICAL,
            'FATAL': logging.FATAL,
            'ERROR': logging.ERROR,
            'WARN': logging.WARNING,
            'WARNING': logging.WARNING,
            'INFO': logging.INFO,
            'DEBUG': logging.DEBUG,
            'NOTSET': logging.NOTSET,
        }
        if level not in string_to_level:
            level = "INFO"
        return string_to_level[level]

    def load_as_settings(self):
        self.AS_HOST = os.getenv("AS_HOST")
        self.AS_PORT = int(os.getenv("AS_PORT"))
        self.AS_LOG_LEVEL = self.logging_level_strint_to_int(os.getenv("AS_LOG_LEVEL"))
        self.AS_LOG_FILE = os.getenv("AS_LOG_FILE")

    def load_as_db(self):
        self.PE_DB_DIALECT = os.getenv("PE_DB_DIALECT")
        self.PE_DB_NOT_ASYNC_DIALECT = os.getenv("PE_DB_NOT_ASYNC_DIALECT")
        self.PE_DB_USERNAME = os.getenv("PE_DB_USERNAME")
        self.PE_DB_PASSWORD = os.getenv("PE_DB_PASSWORD")
        self.PE_DB_HOST = os.getenv("PE_DB_HOST")
        self.PE_DB_PORT = int(os.getenv("PE_DB_PORT"))
        self.PE_DB_DATABASE = os.getenv("PE_DB_DATABASE")
        self.PE_DB_ECHO = os.getenv("PE_DB_ECHO").lower()
        self.PE_DB_ECHO = (self.PE_DB_ECHO == "true" or self.PE_DB_ECHO == "1")


directory = Path(os.path.dirname(os.path.abspath(__file__)))
config = Config(str(directory / ".env"))
