import datetime
from typing import List, Optional
from src.modules.dto.buildings.building_dto import BuildingDto
from src.modules.dto.auditoriums.auditorium_dto import AuditoriumDto
from src.modules.dto.users.user_auditorium_dto import UserAuditoriumDto
from src.modules.dto.auditoriums.auditorium_short_dto import AuditoriumShortDto

from abc import ABC, abstractmethod

from src.modules.dto.users.user_in_audotorium_dto import UserInAuditoriumDto


class HSEClientInterface(ABC):
    def __init__(self):
        ...

    # Building methods
    @abstractmethod
    async def get_buildings(self, page: int, page_size: int) -> List[BuildingDto]:
        ...

    @abstractmethod
    async def get_building_by_id(self, building_id: int) -> Optional[BuildingDto]:
        ...

    @abstractmethod
    async def get_auditoriums_in_building(self, building_id: int) -> Optional[List[AuditoriumShortDto]]:
        ...

    @abstractmethod
    async def get_free_auditoriums_in_building(self, building_id: int, interval_start: datetime.datetime,
                                               interval_end: datetime.datetime,
                                               language="ru") -> Optional[List[AuditoriumShortDto]]:
        ...

    # Auditorium methods
    @abstractmethod
    async def get_short_auditorium_by_id(self, auditorium_id: int) -> Optional[AuditoriumShortDto]:
        ...

    @abstractmethod
    async def get_auditorium_by_id(self, auditorium_id: int) -> Optional[AuditoriumDto]:
        # То же самое, что и с get_lessons_in_auditorium, наверное
        ...
