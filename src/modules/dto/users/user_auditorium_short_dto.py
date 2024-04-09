from src.modules.dto.base_dto import BaseDto
from src.modules.dto.auditoriums.auditorium_dto import AuditoriumDto


class UserAuditoriumShortDto(BaseDto):
    user_id: int
    auditorium: AuditoriumDto
    silent_status: bool  # Если True, то пользователь хочет побыть в тишине
