from sqlalchemy import URL
from src.config import config
from functools import lru_cache


@lru_cache
def get_db_url():
    return URL.create(
        config.PE_DB_DIALECT,
        config.PE_DB_USERNAME,
        config.PE_DB_PASSWORD,
        config.PE_DB_HOST,
        config.PE_DB_PORT,
        config.PE_DB_DATABASE
    )


@lru_cache
def get_not_async_db_url():
    return URL.create(
        config.PE_DB_NOT_ASYNC_DIALECT,
        config.PE_DB_USERNAME,
        config.PE_DB_PASSWORD,
        config.PE_DB_HOST,
        config.PE_DB_PORT,
        config.PE_DB_DATABASE
    )


@lru_cache
def get_db_settings():
    return {
        "not_async_url": get_not_async_db_url(),
        "database_url": get_db_url(),
        "echo": config.PE_DB_ECHO,
    }
