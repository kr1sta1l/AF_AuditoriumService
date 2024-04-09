from typing import Optional
from src.modules.dto.base_dto import BaseDto
from src.modules.dao.user_dao import UserDao


class UserInAuditoriumDto(BaseDto):
    id: int
    silent_status: bool  # Если True, то пользователь хочет побыть в тишине
    end: Optional[str]  # Время окончания нахождения в аудитории

    @staticmethod
    def from_dao(dao: UserDao) -> "UserInAuditoriumDto":
        return UserInAuditoriumDto(id=dao.user_id, silent_status=dao.silent_status, end=dao.end_of_location)
