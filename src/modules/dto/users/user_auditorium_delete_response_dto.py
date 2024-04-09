from src.modules.dto.base_dto import BaseDto
from src.modules.dto.auditoriums.auditorium_dto import AuditoriumDto


class UserAuditoriumDeleteResponseDto(BaseDto):
    user_id: int
    auditorium: AuditoriumDto
