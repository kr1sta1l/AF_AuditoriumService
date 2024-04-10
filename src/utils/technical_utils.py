from src.database.db import get_db_settings
from sqlalchemy.exc import OperationalError
from src.controllers.session import get_engine


async def database_connection_successful() -> bool:
    try:
        db_settings = get_db_settings()
        engine = get_engine()
        async with engine.connect(db_settings["database_url"]):
            return True
    except OperationalError:
        return False
