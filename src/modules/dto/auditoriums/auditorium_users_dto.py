from .auditorium_dto import AuditoriumDto


class AuditoriumUsersDto(AuditoriumDto):
    noise_users_amount: int
    silent_users_amount: int

    @staticmethod
    def from_auditorium_dto(auditorium_dto: AuditoriumDto) -> "AuditoriumUsersDto":
        return AuditoriumUsersDto(id=auditorium_dto.id, name=auditorium_dto.name,
                                  capacity=auditorium_dto.capacity,
                                  sockets_amount=auditorium_dto.sockets_amount,
                                  projector=auditorium_dto.projector, type=auditorium_dto.type,
                                  corpus=auditorium_dto.corpus, building=auditorium_dto.building,
                                  noise_users_amount=0, silent_users_amount=0)
