from typing import List, Sequence, Optional
from src.modules.dao.user_dao import UserDao
from src.controllers.session import get_user_repository
from src.modules.dto.auditoriums.auditorium_dto import AuditoriumDto
from src.modules.dto.auditoriums.auditorium_short_dto import AuditoriumShortDto
from src.modules.dto.auditoriums.auditorium_users_dto import AuditoriumUsersDto
from src.modules.dto.auditoriums.auditorium_short_users_dto import AuditoriumShortUsersDto


async def get_auditoriums_with_users(auditorium_list: List[AuditoriumShortDto],
                                     noise_users_presence: bool = True, corpus_id: Optional[int] = None) -> List[
    AuditoriumShortUsersDto]:
    result_list: List[AuditoriumShortUsersDto] = []
    user_repository = get_user_repository()

    for auditorium in auditorium_list:
        if corpus_id is not None:
            if auditorium.corpus.id != corpus_id:
                continue
        users: Sequence[UserDao] = await user_repository.get_all_by_whereclause(
            UserDao.auditorium_id == auditorium.id)
        noise_users_presence_in_auditorium = False
        noise_users_amount = 0
        silent_users_amount = 0
        for user in users:
            if not user.silent_status:
                noise_users_amount += 1
                if not noise_users_presence:
                    noise_users_presence_in_auditorium = True
                    break
            else:
                silent_users_amount += 1
        auditorium_users: AuditoriumShortUsersDto = AuditoriumShortUsersDto.from_auditorium_dto(auditorium)
        auditorium_users.noise_users_amount = noise_users_amount
        auditorium_users.silent_users_amount = silent_users_amount
        if not noise_users_presence_in_auditorium:
            result_list.append(auditorium_users)
    result_list.sort(key=lambda x: (x.silent_users_amount, x.noise_users_amount, x.name), reverse=True)
    return result_list


async def get_auditorium_with_users(auditorium: AuditoriumDto) -> AuditoriumUsersDto:
    user_repository = get_user_repository()

    noise_users_amount = 0
    silent_users_amount = 0

    users: Sequence[UserDao] = await user_repository.get_all_by_whereclause(
        UserDao.auditorium_id == auditorium.id, page=0, page_size=100)
    for user in users:
        if not user.silent_status:
            noise_users_amount += 1
        else:
            silent_users_amount += 1
    auditorium_users: AuditoriumUsersDto = AuditoriumUsersDto.from_auditorium_dto(auditorium)
    auditorium_users.noise_users_amount = noise_users_amount
    auditorium_users.silent_users_amount = silent_users_amount
    return auditorium_users
