import os
import logging
from pathlib import Path
from pydantic import Field
from typing import Optional, AnyStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class PydanticConfig(BaseSettings):
    # model_config = SettingsConfigDict(env_file=Path(os.path.dirname(os.path.realpath(__file__))) / '.env',
    #                                   env_file_encoding='utf-8')

    AS_HOST: Optional[AnyStr] = Field("0.0.0.0", env="AS_HOST")
    AS_PORT: Optional[int] = Field("8000", env="AS_PORT")
    AS_LOG_LEVEL: Optional[AnyStr] = Field("INFO", env="AS_LOG_LEVEL")
    AS_LOG_FILE: Optional[AnyStr] = Field(None, env="AS_LOG_FILE")

    AUD_DB_DIALECT: Optional[AnyStr] = Field("postgresql+asyncpg", env="AUD_DB_DIALECT")
    AUD_DB_NOT_ASYNC_DIALECT: Optional[AnyStr] = Field("postgresql", env="AUD_DB_NOT_ASYNC_DIALECT")
    AUD_DB_USERNAME: Optional[AnyStr] = Field("postgres", env="AUD_DB_USERNAME")
    AUD_DB_PASSWORD: Optional[AnyStr] = Field("postgres", env="AUD_DB_PASSWORD")
    AUD_DB_HOST: Optional[AnyStr] = Field("localhost", env="AUD_DB_HOST")
    AUD_DB_PORT: Optional[int] = Field(5432, env="AUD_DB_PORT")
    AUD_DB_DATABASE: Optional[AnyStr] = Field("auditorium_service", env="AUD_DB_DATABASE")
    AUD_DB_ECHO: Optional[bool] = Field(False, env="AUD_DB_ECHO")

    RB_CONNECTION_HOST: Optional[AnyStr] = Field("localhost", env="RB_CONNECTION_HOST")
    RB_CONNECTION_PORT: Optional[int] = Field(5672, env="RB_CONNECTION_PORT")
    RB_USERNAME: Optional[AnyStr] = Field("guest", env="RB_USERNAME")
    RB_PASSWORD: Optional[AnyStr] = Field("guest", env="RB_PASSWORD")
    RB_VIRTUAL_HOST: Optional[AnyStr] = Field("/", env="RB_VIRTUAL_HOST")
    LISTEN_QUEUE: Optional[AnyStr] = Field("profile-delete-aud-queue", env="LISTEN_QUEUE")
    SEND_QUEUE: Optional[AnyStr] = Field("auditorium-update-queue", env="SEND_QUEUE")
    EXCHANGE: Optional[AnyStr] = Field("", env="EXCHANGE")

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


config = PydanticConfig()
