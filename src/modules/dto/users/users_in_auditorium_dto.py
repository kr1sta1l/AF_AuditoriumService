from typing import List
from src.modules.dto.base_dto import BaseDto
from src.modules.dto.auditoriums.auditorium_dto import AuditoriumDto
from .user_in_audotorium_dto import UserInAuditoriumDto


class UsersInAuditoriumDto(BaseDto):
    auditorium: AuditoriumDto
    users: List[UserInAuditoriumDto]
    noise_users_amount: int
    silence_users_amount: int
