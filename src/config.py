import os
import logging
from pathlib import Path
from pydantic import Field
from typing import Optional, AnyStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class PydanticConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path(os.path.dirname(os.path.realpath(__file__))) / '.env2',
                                      env_file_encoding='utf-8')

    AS_HOST: Optional[AnyStr] = Field(None, env="AS_HOST")
    AS_PORT: Optional[int] = Field(None, env="AS_PORT")
    AS_LOG_LEVEL: Optional[AnyStr] = Field(None, env="AS_LOG_LEVEL")
    AS_LOG_FILE: Optional[AnyStr] = Field(None, env="AS_LOG_FILE")

    PE_DB_DIALECT: Optional[AnyStr] = Field(None, env="PE_DB_DIALECT")
    PE_DB_NOT_ASYNC_DIALECT: Optional[AnyStr] = Field(None, env="PE_DB_NOT_ASYNC_DIALECT")
    PE_DB_USERNAME: Optional[AnyStr] = Field(None, env="PE_DB_USERNAME")
    PE_DB_PASSWORD: Optional[AnyStr] = Field(None, env="PE_DB_PASSWORD")
    PE_DB_HOST: Optional[AnyStr] = Field(None, env="PE_DB_HOST")
    PE_DB_PORT: Optional[int] = Field(None, env="PE_DB_PORT")
    PE_DB_DATABASE: Optional[AnyStr] = Field(None, env="PE_DB_DATABASE")
    PE_DB_ECHO: Optional[bool] = Field(None, env="PE_DB_ECHO")
    USER_SERVICE_HOST: Optional[AnyStr] = Field(None, env="USER_SERVICE_HOST")
    USER_SERVICE_PORT: Optional[int] = Field(None, env="USER_SERVICE_PORT")

    RB_CONNECTION_HOST: Optional[AnyStr] = Field("localhost", env="RB_CONNECTION_HOST")
    RB_CONNECTION_PORT: Optional[int] = Field(5672, env="RB_CONNECTION_PORT")
    LISTEN_QUEUE: Optional[AnyStr] = Field("profile-delete-aud-queue", env="LISTEN_QUEUE")
    SEND_QUEUE: Optional[AnyStr] = Field("auditorium-update-queue", env="SEND_QUEUE")
    EXCHANGE: Optional[AnyStr] = Field("", env="EXCHANGE")
    RB_USERNAME: Optional[AnyStr] = Field("guest", env="RB_USERNAME")
    RB_PASSWORD: Optional[AnyStr] = Field("guest", env="RB_PASSWORD")
    RB_VIRTUAL_HOST: Optional[AnyStr] = Field("/", env="RB_VIRTUAL_HOST")

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


directory = Path(os.path.dirname(os.path.abspath(__file__)))
config = PydanticConfig()
