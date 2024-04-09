from src.modules.dto.base_dto import BaseDto
from src.modules.dto.corpus_dto import Corpus


class BuildingShortDto(BaseDto):
    id: int
    city: str
    address: str
