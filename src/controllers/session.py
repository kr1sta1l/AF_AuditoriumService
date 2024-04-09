from functools import lru_cache
from src.modules.dao import BaseDao
from src.modules.dao import UserDao
from sqlalchemy import create_engine
from src.database.db import get_db_settings
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy_utils import database_exists, create_database
from src.repository.generic_repository import GenericRepository as GenericRepo

__db_settings = get_db_settings()
__not_async_engine = create_engine(__db_settings["not_async_url"], echo=__db_settings["echo"])
if not database_exists(__not_async_engine.url):
    create_database(__not_async_engine.url)

__engine = create_async_engine(__db_settings["database_url"], echo=__db_settings["echo"])


@lru_cache
def get_user_repository():
    return GenericRepo[UserDao](UserDao, __engine)


async def init_db():
    async with __engine.begin() as conn:
        await conn.run_sync(BaseDao.metadata.drop_all)
        await conn.run_sync(BaseDao.metadata.create_all)
