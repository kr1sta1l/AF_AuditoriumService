from src.modules.dto.base_dto import BaseDto
from src.modules.dto.corpus_dto import Corpus


class AuditoriumShortDto(BaseDto):
    id: int
    # Название аудитории (номер крч)
    name: str

    # Вместимость студентов
    capacity: int

    # Количество розеток
    sockets_amount: int

    # Наличие проекторов
    projector: bool
    # status: str  # че это?

    # тип аудитории (lecture(лекционная), language(языковая), specialized(специализированная),
    # seminar(семинарская), laboratory, и т.п.(another)) - видимо, это вместо статуса
    type: str

    # Корпус
    corpus: Corpus
