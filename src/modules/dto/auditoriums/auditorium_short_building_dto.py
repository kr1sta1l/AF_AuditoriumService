from src.modules.dto.buildings.building_short_dto import BuildingShortDto
from .auditorium_short_dto import AuditoriumShortDto
from .auditorium_dto import AuditoriumDto


class AuditoriumShortBuildingDto(AuditoriumShortDto):
    # Название здания
    building: BuildingShortDto

    @staticmethod
    def from_dto(dto: AuditoriumDto) -> "AuditoriumShortBuildingDto":
        return AuditoriumShortBuildingDto(id=dto.id, name=dto.name, capacity=dto.capacity,
                                          sockets_amount=dto.sockets_amount, projector=dto.projector,
                                          type=dto.type, corpus=dto.corpus, building=BuildingShortDto(
                                                                                   id=dto.building.id,
                                                                                   city=dto.building.city,
                                                                                   address=dto.building.address))
