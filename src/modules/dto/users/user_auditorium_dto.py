import logging
import datetime
from typing import Optional
from pydantic import field_validator, constr
from .user_auditorium_short_dto import UserAuditoriumShortDto


class UserAuditoriumDto(UserAuditoriumShortDto):
    end: Optional[constr(pattern=r'^\d{4}-\d{2}-\d{2}-\d{2}-\d{2}$')] = None  # по умолчанию пусто

    @field_validator("end")
    def check_date_format(cls, date_string):
        if date_string is None:
            return None

        logging.error("date is not None")
        date_format = "%Y-%m-%d-%H-%M"
        try:
            datetime.datetime.strptime(date_string, date_format)
        except ValueError:
            raise ValueError(f"Incorrect date format, should be {date_format}")
        logging.error("correct date format")

        if date_string < datetime.datetime.now().strftime(date_format):
            raise ValueError("|Can't set end date in the past|")
        logging.error("end date is not in the past")
        return date_string
