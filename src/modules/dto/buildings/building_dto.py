from src.modules.dto.corpus_dto import Corpus
from src.modules.dto.buildings.building_short_dto import BuildingShortDto


class BuildingDto(BuildingShortDto):
    first_lesson_start: str
    last_lesson_end: str
    lesson_length_minutes: int
    corpus_list: list[Corpus]
