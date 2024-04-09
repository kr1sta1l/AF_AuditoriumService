from .auditorium_short_dto import AuditoriumShortDto


class AuditoriumShortUsersDto(AuditoriumShortDto):
    noise_users_amount: int
    silent_users_amount: int

    @staticmethod
    def from_auditorium_dto(auditorium_short_dto: AuditoriumShortDto) -> "AuditoriumShortUsersDto":
        return AuditoriumShortUsersDto(id=auditorium_short_dto.id, name=auditorium_short_dto.name,
                                       capacity=auditorium_short_dto.capacity,
                                       sockets_amount=auditorium_short_dto.sockets_amount,
                                       projector=auditorium_short_dto.projector, type=auditorium_short_dto.type,
                                       corpus=auditorium_short_dto.corpus, noise_users_amount=0, silent_users_amount=0)
