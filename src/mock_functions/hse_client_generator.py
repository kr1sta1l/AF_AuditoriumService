import random
from typing import List, Dict

from src.modules.dto.buildings.building_dto import BuildingDto
from src.modules.dto.corpus_dto import Corpus

from src.modules.dto.auditoriums.auditorium_dto import AuditoriumDto


class HSEClientGenerator:
    def __init__(self):
        self.buildings: List[BuildingDto] = []
        self.auditoriums: Dict[int, List[AuditoriumDto]] = {}

        self._building_auditorium_id_multiplier = 10000

        self._building_generator()
        self._auditorium_generator()

    def building_id_from_auditorium_id(self, auditorium_id: int) -> int:
        return auditorium_id // self._building_auditorium_id_multiplier

    def _building_generator(self):
        self.buildings: List[BuildingDto] = []
        lessons_start_end = [
            ("08-00", "21-00", 90),
            ("09-30", "21-00", 90),
        ]
        corpus_names = ["{corpus}", "{floor}", "{building_c}"]
        available_cities = ["moscow", "saint-petersburg", "nizhny-novgorod", "perm"]
        for i in range(20):
            lesson_start_end = random.choice(lessons_start_end)
            corpus_name = random.choice(corpus_names)
            corpus_list: List[Corpus] = []
            for j in range(random.randint(5, 9)):
                corpus_list.append(Corpus(id=j, name=str(chr(65 + j))))
                # name=corpus_name + " " + str(chr(65 + j))))
                # corpus_list[j] = corpus_name + " " + str(j)
            self.buildings.append(BuildingDto(
                id=i,
                name='{building_name} ' + str(i),
                city=random.choice(available_cities),
                address='{building_address} ' + str(i),
                first_lesson_start=lesson_start_end[0],
                last_lesson_end=lesson_start_end[1],
                lesson_length_minutes=lesson_start_end[2],
                corpus_list=corpus_list
            ))

    def _auditorium_generator(self):
        for building in self.buildings:
            self.auditoriums[building.id] = []
            for i in range(random.randint(70, 120)):
                corpus: Corpus = random.choice(building.corpus_list)
                self.auditoriums[building.id].append(AuditoriumDto(
                    id=building.id * self._building_auditorium_id_multiplier + i,
                    # name="{auditorium} " + str(i),
                    name=str(i),
                    capacity=random.randint(15, 40),
                    sockets_amount=random.randint(2, 10),
                    projector=random.choice([True, False]),
                    type=random.choice(
                        ["lecture", "language", "specialized", "seminar", "laboratory", "computer"]),
                    corpus=Corpus(id=corpus.id, name=corpus.name),
                    building=building
                ))

    def display_auditoriums(self):
        for building_id, auditoriums in self.auditoriums.items():
            print(f"Building {building_id}:")
            for auditorium in auditoriums:
                print(auditorium)
            print()


if __name__ == "__main__":
    generator = HSEClientGenerator()
    generator.display_auditoriums()
