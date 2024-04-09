from .building_dto import BuildingDto
from src.modules.dto.base_dto import BaseDto
from src.modules.dto.auditoriums.auditorium_short_users_dto import AuditoriumShortUsersDto


class BuildingAuditoriumsDto(BaseDto):
    building: BuildingDto
    auditoriums: list[AuditoriumShortUsersDto]
