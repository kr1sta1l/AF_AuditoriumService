import random
import datetime
from typing import List, Optional, Tuple, Dict

from src.modules.dto.corpus_dto import Corpus
from .hse_client_interface import HSEClientInterface
from src.modules.dto.buildings.building_dto import BuildingDto
from src.modules.dto.auditoriums.auditorium_dto import AuditoriumDto
from src.modules.dto.auditoriums.auditorium_short_dto import AuditoriumShortDto

from src.mock_functions.hse_client_generator import HSEClientGenerator


class HSEClientMock(HSEClientInterface):
    def __init__(self, seed=42):
        super().__init__()
        self.seed = seed
        random.seed(self.seed)
        self.client_generator = HSEClientGenerator()

        self.language_dict = {
            "ru": {"address": "Адрес", "auditorium": ["Аудитория", "Кабинет"],
                   "corpus": "Корпус", "floor": "Этаж", "building_c": "Здание",
                   "city": {"moscow": "Москва", "saint-petersburg": "Санкт-Петербург",
                            "nizhny-novgorod": "Нижний Новгород", "perm": "Пермь"},
                   "auditorium_type": {
                       "lecture": "Лекционная", "language": "Языковая", "specialized": "Специализированная",
                       "seminar": "Семинарская", "laboratory": "Лаборатория",
                       "computer": "Компьютерная"}
                   },
            "en": {"address": "Address", "auditorium": ["Auditorium", "Cabinet"],
                   "corpus": "Corpus", "floor": "Floor", "building_c": "Building",
                   "city": {"moscow": "Moscow", "saint-petersburg": "Saint-Petersburg",
                            "nizhny-novgorod": "Nizhny Novgorod", "perm": "Perm"},
                   "auditorium_type": {
                       "lecture": "Lecture", "language": "Language", "specialized": "Specialized",
                       "seminar": "Seminar", "laboratory": "Laboratory",
                       "computer": "Computer"}
                   }
        }

    def translate_building(self, building: BuildingDto, language: str) -> None:
        building.address = building.address.format(building_address=self.language_dict[language]["address"])
        building.city = self.language_dict[language]["city"][building.city]
        for i, corpus in enumerate(building.corpus_list):
            # corpus_id: int = corpus.id
            corpus_name: str = corpus.name
            if "{corpus}" in corpus_name:
                corpus.name = corpus_name.format(corpus=self.language_dict[language]["corpus"])
            if "{floor}" in corpus_name:
                corpus.name = corpus_name.format(floor=self.language_dict[language]["floor"])
            if "{building_c}" in corpus_name:
                corpus.name = corpus_name.format(
                    building_c=self.language_dict[language]["building_c"])

    def translate_auditorium(self, auditorium: AuditoriumShortDto | AuditoriumDto, language: str) -> None:
        auditorium.name = auditorium.name.format(auditorium=random.choice(self.language_dict[language]["auditorium"]))
        auditorium.type = self.language_dict[language]["auditorium_type"][auditorium.type]
        corpus_name: str = auditorium.corpus.name
        if "{corpus}" in corpus_name:
            auditorium.corpus.name = corpus_name.format(corpus=self.language_dict[language]["corpus"])
        if "{floor}" in corpus_name:
            auditorium.corpus.name = corpus_name.format(floor=self.language_dict[language]["floor"])
        if "{building_c}" in corpus_name:
            auditorium.corpus.name = corpus_name.format(building_c=self.language_dict[language]["building_c"])

    async def get_buildings(self, page: int = 1, page_size: int = 10, language: str = "ru"
                            ) -> Dict[str, List[BuildingDto] | int]:
        # generate 60 random buildings and return paginated list of them
        if language not in self.language_dict.keys():
            language = "ru"
        buildings: List[BuildingDto] = []
        for building in self.client_generator.buildings:
            corpus_list_clone = [Corpus(id=corpus.id, name=corpus.name) for corpus in building.corpus_list]
            building_clone = BuildingDto(id=building.id, city=building.city,
                                         address=building.address,
                                         first_lesson_start=building.first_lesson_start,
                                         last_lesson_end=building.last_lesson_end,
                                         lesson_length_minutes=building.lesson_length_minutes,
                                         corpus_list=corpus_list_clone)
            self.translate_building(building_clone, language)
            buildings.append(building_clone)

        buildings.sort(key=lambda x: (x.city, x.address))

        pages_amount: int = len(buildings) // page_size
        if len(buildings) % page_size != 0:
            pages_amount += 1

        return {"buildings": buildings[(page - 1) * page_size: page * page_size], "pages_amount": pages_amount,
                "buildings_amount": len(buildings)}

    async def get_building_by_id(self, building_id: int, language: str = "ru") -> Optional[BuildingDto]:
        building = list(filter(lambda x: x.id == building_id, self.client_generator.buildings))
        if len(building) == 0:
            return None
        building_clone = BuildingDto(id=building[0].id, city=building[0].city,
                                     address=building[0].address,
                                     first_lesson_start=building[0].first_lesson_start,
                                     last_lesson_end=building[0].last_lesson_end,
                                     lesson_length_minutes=building[0].lesson_length_minutes,
                                     corpus_list=building[0].corpus_list)
        self.translate_building(building_clone, language)
        return building_clone

    async def get_auditoriums_in_building(self, building_id: int, language="ru") -> List[AuditoriumShortDto]:
        auditoriums = self.client_generator.auditoriums[building_id]
        auditoriums_clone = []
        for auditorium in auditoriums:
            auditorium_clone = AuditoriumShortDto(id=auditorium.id, name=auditorium.name, capacity=auditorium.capacity,
                                                  sockets_amount=auditorium.sockets_amount,
                                                  projector=auditorium.projector,
                                                  type=auditorium.type,
                                                  corpus=Corpus(id=auditorium.corpus.id, name=auditorium.corpus.name))
            self.translate_auditorium(auditorium_clone, language=language)
            auditoriums_clone.append(auditorium_clone)
        return auditoriums_clone

    async def get_free_auditoriums_in_building(self, building_id: int, interval_start: datetime.datetime,
                                               interval_end: datetime.datetime, page: int = 1, page_size: int = 10,
                                               language="ru"
                                               ) -> Tuple[Optional[List[AuditoriumShortDto]], int, int, int]:

        unique_id: int = int(
            str(interval_start.strftime("%Y%m%d%H")) + str(interval_end.strftime("%Y%m%d%H")) + str(building_id))
        auditoriums: List[AuditoriumShortDto] = await self.get_auditoriums_in_building(building_id,
                                                                                       language=language)
        auditoriums_amount: int = len(auditoriums)

        if auditoriums is None:
            return None, 0, 0, 0

        result_auditoriums: List[AuditoriumShortDto] = []

        random.seed(unique_id)
        for auditorium in auditoriums:
            if random.random() < 0.15:
                result_auditoriums.append(auditorium)

        result_auditoriums_amount: int = len(result_auditoriums)
        random.seed(self.seed)

        pages_amount: int = result_auditoriums_amount // page_size
        if result_auditoriums_amount % page_size != 0:
            pages_amount += 1
        result_auditoriums = result_auditoriums[(page - 1) * page_size: page * page_size]

        return result_auditoriums, auditoriums_amount, result_auditoriums_amount, pages_amount

    async def _get_auditorium_by_id_from_generator(self, auditorium_id: int, language="ru") -> Optional[AuditoriumDto]:
        building: Optional[BuildingDto] = await self.get_building_by_id(
            self.client_generator.building_id_from_auditorium_id(auditorium_id), language=language)
        if building is None:
            return None

        auditorium = list(filter(lambda x: x.id == auditorium_id, self.client_generator.auditoriums[building.id]))
        if len(auditorium) == 0:
            return None

        auditorium_clone = AuditoriumDto(id=auditorium[0].id, name=auditorium[0].name, capacity=auditorium[0].capacity,
                                         sockets_amount=auditorium[0].sockets_amount, projector=auditorium[0].projector,
                                         type=auditorium[0].type, corpus=auditorium[0].corpus,
                                         building=building)
        self.translate_auditorium(auditorium_clone, language=language)

        return auditorium_clone

    async def get_short_auditorium_by_id(self, auditorium_id: int) -> Optional[AuditoriumShortDto]:
        auditorium: Optional[AuditoriumDto] = await self._get_auditorium_by_id_from_generator(auditorium_id)
        if auditorium is None:
            return None
        return AuditoriumShortDto(id=auditorium.id, name=auditorium.name, capacity=auditorium.capacity,
                                  sockets_amount=auditorium.sockets_amount, projector=auditorium.projector,
                                  type=auditorium.type, corpus=auditorium.corpus)

    async def get_auditorium_by_id(self, auditorium_id: int, language="ru") -> Optional[AuditoriumDto]:
        return await self._get_auditorium_by_id_from_generator(auditorium_id, language=language)
