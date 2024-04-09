from src.modules.dto.base_dto import BaseDto
from src.modules.dto.corpus_dto import Corpus


class BuildingDto(BaseDto):
    id: int
    city: str
    address: str
    first_lesson_start: str
    last_lesson_end: str
    lesson_length_minutes: int
    # corpus_list: dict[int, str]
    corpus_list: list[Corpus]
