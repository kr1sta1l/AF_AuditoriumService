import datetime
from sqlalchemy import Integer, Boolean, DateTime
from sqlalchemy.orm import mapped_column, MappedColumn
from typing import Optional

from .base_dao import BaseDao


class UserDao(BaseDao):
    __tablename__ = "users"

    user_id: MappedColumn[int] = mapped_column("user_id", Integer, primary_key=True, nullable=False)
    auditorium_id: MappedColumn[Optional[int]] = mapped_column("auditorium_id", Integer, nullable=False,
                                                               unique=False)
    silent_status: MappedColumn[Optional[bool]] = mapped_column("silent_status", Boolean, nullable=False)
    end_of_location: MappedColumn[Optional[datetime.datetime]] = mapped_column("end_of_location", DateTime,
                                                                               nullable=True)
