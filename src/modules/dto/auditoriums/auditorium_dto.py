from src.modules.dto.buildings.building_dto import BuildingDto
from .auditorium_short_dto import AuditoriumShortDto


class AuditoriumDto(AuditoriumShortDto):
    # Название здания
    building: BuildingDto
