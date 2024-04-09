from src.modules.dto.base_dto import BaseDto


class UserAuditoriumShortRequestDto(BaseDto):
    auditorium_id: int
    silent_status: bool  # Если True, то пользователь хочет побыть в тишине
