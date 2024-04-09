import logging
import datetime

from fastapi.responses import JSONResponse
from typing import Optional, Tuple, List, Any, Sequence
from fastapi import APIRouter, Query, Header, HTTPException, Depends

from src.modules.dao.user_dao import UserDao
from src.hse_api_client import hse_api_client
from pydantic.alias_generators import to_camel
from src.controllers.session import get_user_repository
from src.api_adapter.user_service import UserServiceClient
from src.modules.dto.buildings.building_dto import BuildingDto
from src.repository.generic_repository import GenericRepository
from src.modules.dto.auditoriums.auditorium_dto import AuditoriumDto
from src.modules.dto.responses.default_response import DefaultResponse
from src.modules.dto.users.user_auditorium_dto import UserAuditoriumDto
from src.modules.dto.users.user_in_audotorium_dto import UserInAuditoriumDto
from src.modules.dto.users.users_in_auditorium_dto import UsersInAuditoriumDto
from src.modules.dto.auditoriums.auditorium_short_dto import AuditoriumShortDto
from src.modules.dto.auditoriums.auditorium_users_dto import AuditoriumUsersDto
from src.modules.dto.buildings.building_auditoriums_dto import BuildingAuditoriumsDto
from src.modules.dto.users.user_auditorium_short_request_dto import UserAuditoriumShortRequestDto
from src.utils.add_user_to_auditorium_notificator import send_notification_about_user_in_auditorium
from src.utils.auditorium_route_utils import get_auditoriums_with_users, get_auditorium_with_users
from src.modules.dto.users.user_auditorium_delete_response_dto import UserAuditoriumDeleteResponseDto
from src.modules.dto.responses.auditorium_user_error_response import AuditoriumUserErrorResponse
from src.modules.dto.auditoriums.auditorium_short_users_dto import AuditoriumShortUsersDto

router = APIRouter()


@router.get("/building/{building_id}",
            description="Get list of free auditoriums in building. Included in headers: "
                        "pages_amount - amount of pages, "
                        "entities_amount - amount of entities in response, "
                        "auditoriums_amount - amount of auditoriums in building",
            summary="Get list of free auditoriums in building",
            responses={200: {"description": "OK", "model": BuildingAuditoriumsDto},
                       404: {"description": "Building not found", "model": DefaultResponse},
                       409: {"description": "Incorrect interval", "model": DefaultResponse}},
            response_model=BuildingAuditoriumsDto)
async def get_building_auditoriums(building_id: int,
                                   noise_users_presence: bool = Query(True,
                                                                      description="If False, then return only "
                                                                                  "auditoriums with silent users in "
                                                                                  "it",
                                                                      alias=to_camel("noise_users_presence")),
                                   corpus_id: Optional[int] = Query(None,
                                                                    description="Corpus id. If None, search in all "
                                                                                "corpuses",
                                                                    alias=to_camel("corpus_id")),
                                   interval_start: str = Query(..., regex=r'^\d{4}-\d{2}-\d{2}-\d{2}-\d{2}$',
                                                               description="Start time, format: \"YYYY-MM-DD-HH-MM\"",
                                                               alias=to_camel("interval_start")),
                                   interval_end: str = Query(..., regex=r'^\d{4}-\d{2}-\d{2}-\d{2}-\d{2}$',
                                                             description="End time, format: \"YYYY-MM-DD-HH-MM\"",
                                                             alias=to_camel("interval_end")),
                                   language_code: str = Query("ru", description="Language code",
                                                              alias=to_camel("language_code")),
                                   page: int = Query(ge=0, default=0, alias=to_camel("page")),
                                   size: int = Query(ge=1, le=100, default=10, alias=to_camel("size"))) -> Any:
    page += 1
    logging.info(f"{building_id}, {noise_users_presence}, {interval_start}, {interval_end}, {page}, {size}")

    # "YYYY-MM-DD-HH-MM"
    datetime_format = "%Y-%m-%d-%H-%M"
    interval_start_dt = datetime.datetime.strptime(interval_start, datetime_format)
    interval_end_dt = datetime.datetime.strptime(interval_end, datetime_format)

    if interval_start_dt >= interval_end_dt:
        raise HTTPException(status_code=409, detail="Incorrect interval")

    building: BuildingDto = await hse_api_client.get_building_by_id(building_id, language=language_code)
    if building is None:
        raise HTTPException(status_code=404, detail=f"Building {building_id} not found")

    free_auditoriums_info: Tuple[
        List[AuditoriumShortDto], int, int, int] = \
        await hse_api_client.get_free_auditoriums_in_building(building_id, interval_start_dt, interval_end_dt,
                                                              page=page, page_size=size, language=language_code)
    auditorium_list: List[AuditoriumShortDto] = free_auditoriums_info[0]
    result_auditorium_list: List[AuditoriumShortUsersDto] = await get_auditoriums_with_users(auditorium_list,
                                                                                             noise_users_presence,
                                                                                             corpus_id)

    result: BuildingAuditoriumsDto = BuildingAuditoriumsDto(building=building, auditoriums=result_auditorium_list)
    headers = {"auditoriums_amount": str(free_auditoriums_info[1]),
               "entities_amount": str(free_auditoriums_info[2]),
               "pages_amount": str(free_auditoriums_info[3])}
    return JSONResponse(headers=headers, content=result.model_dump(mode='json', by_alias=True),
                        media_type="application/json")


@router.get("/user", responses={200: {"description": "OK", "model": UserAuditoriumDto},
                                404: {"description": "User not found", "model": DefaultResponse},
                                409: {"description": "User not in any auditorium", "model": DefaultResponse}},
            description="Get auditorium where user located in", summary="Get auditorium where user located in")
async def get_user_auditorium(user_id: int = Header(alias=to_camel("user_id")),
                              language_code: str = Query("ru", description="Language code",
                                                         alias=to_camel("language_code")),  # ) -> str:  # ,
                              user_repository: GenericRepository = Depends(get_user_repository)) -> UserAuditoriumDto:
    user_dao: Optional[UserDao] = await user_repository.get_one_by_whereclause(UserDao.user_id == user_id)
    if user_dao is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    if user_dao.auditorium_id is None:
        raise HTTPException(status_code=409, detail=f"User {user_id} not in any auditorium")

    auditorium_dto: Optional[AuditoriumDto] = await hse_api_client.get_auditorium_by_id(user_dao.auditorium_id,
                                                                                        language=language_code)
    if auditorium_dto is None:
        raise HTTPException(status_code=400, detail=f"Auditorium {user_dao.auditorium_id} not found")

    user_auditorium_dto: UserAuditoriumDto = UserAuditoriumDto(user_id=user_dao.user_id, auditorium=auditorium_dto,
                                                               silent_status=user_dao.silent_status,
                                                               end=user_dao.end_of_location)
    return user_auditorium_dto


@router.get("/info/{auditorium_id}", description="Get auditorium by id", summary="Get auditorium by id",
            responses={200: {"description": "OK", "model": AuditoriumUsersDto},
                       404: {"description": "Auditorium not found", "model": DefaultResponse}})
async def get_auditorium_by_id(auditorium_id: int,
                               language_code: str = Query("ru", description="Language code",
                                                          alias=to_camel("language_code"))) -> AuditoriumUsersDto:
    logging.info(auditorium_id)
    auditorium: AuditoriumDto = await hse_api_client.get_auditorium_by_id(auditorium_id, language=language_code)
    if auditorium is None:
        raise HTTPException(status_code=404, detail=f"Auditorium {auditorium_id} not found")

    auditorium_users: AuditoriumUsersDto = await get_auditorium_with_users(auditorium)
    return auditorium_users


# list of users in auditorium
@router.get("/info/{auditorium_id}/users",
            description="Get list of users in auditorium. Included in headers: "
                        "pages_amount - amount of pages, "
                        "entities_amount - amount of entities in response",
            summary="Get list of users in auditorium",
            responses={200: {"description": "OK", "model": UsersInAuditoriumDto},
                       404: {"description": "Auditorium not found", "model": DefaultResponse}})
async def get_auditorium_users(auditorium_id: int, page: int = Query(ge=0, default=0, alias=to_camel("page")),
                               size: int = Query(ge=1, le=100, default=50, alias=to_camel("size")),
                               language_code: str = Query("ru", description="Language code",
                                                          alias=to_camel("language_code")),
                               user_repository: GenericRepository = Depends(
                                   get_user_repository)) -> Any:
    logging.info(f"{auditorium_id}, {page}, {size}")

    auditorium: AuditoriumDto = await hse_api_client.get_auditorium_by_id(auditorium_id, language=language_code)
    if auditorium is None:
        raise HTTPException(status_code=404, detail=f"Auditorium {auditorium_id} not found")

    user_dao_list: Sequence[UserDao] = await user_repository.get_all_by_whereclause(
        UserDao.auditorium_id == auditorium_id)  # , page=page, page_size=size)

    user_in_auditorium_list: List[UserInAuditoriumDto] = []
    noise_users_amount: int = 0
    silent_users_amount: int = 0
    offset = page * size
    for i, user_dao in enumerate(user_dao_list):
        if offset <= i < offset + size:
            user_in_auditorium_list.append(UserInAuditoriumDto.from_dao(user_dao))
        if user_dao.silent_status:
            silent_users_amount += 1
        else:
            noise_users_amount += 1

    users_in_auditorium_dto: UsersInAuditoriumDto = UsersInAuditoriumDto(auditorium=auditorium,
                                                                         users=user_in_auditorium_list,
                                                                         noise_users_amount=noise_users_amount,
                                                                         silence_users_amount=silent_users_amount)

    users_amount: int = silent_users_amount + noise_users_amount
    pages_amount: int = users_amount // size
    if users_amount % size != 0:
        pages_amount += 1

    headers = {"pages_amount": str(pages_amount), "entities_amount": str(users_amount)}
    return JSONResponse(headers=headers, content=users_in_auditorium_dto.model_dump(mode='json', by_alias=True))


@router.post("/users/add_user", responses={200: {"description": "OK", "model": UserAuditoriumDto},
                                           400: {"description": "EndOfLocation must be not in the past",
                                                 "model": DefaultResponse},
                                           404: {"description": "User/Classroom not found",
                                                 "model": AuditoriumUserErrorResponse}},
             description="Add user to auditorium.",
             summary="Add user to auditorium")
async def add_user_to_auditorium(user_short_dto: UserAuditoriumShortRequestDto,
                                 user_id: int = Header(alias=to_camel("user_id")),
                                 end_of_location: Optional[str] = Query(None,
                                                                        regex=r'^\d{4}-\d{2}-\d{2}-\d{2}-\d{2}$',
                                                                        description="End date, format: "
                                                                                    "\"YYYY-MM-DD-HH-MM\". "
                                                                                    "Default: None",
                                                                        alias=to_camel("end_of_location")),
                                 language_code: str = Query("ru", description="Language code",
                                                            alias=to_camel("language_code")),
                                 user_repository: GenericRepository = Depends(
                                     get_user_repository)) -> UserAuditoriumDto:
    logging.info(f"{user_short_dto}, {user_id}, {end_of_location}")
    if not await UserServiceClient.is_user_exits(user_id):
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    end_of_location_dt: Optional[datetime.datetime] = None
    if end_of_location is not None:
        datetime_format = "%Y-%m-%d-%H-%M"
        end_of_location_dt = datetime.datetime.strptime(end_of_location, datetime_format)

    auditorium: Optional[AuditoriumDto] = await hse_api_client.get_auditorium_by_id(user_short_dto.auditorium_id,
                                                                                    language=language_code)
    if auditorium is None:
        raise HTTPException(status_code=404, detail=f"Auditorium {user_short_dto.auditorium_id} not found")

    # если пользователь в другой аудитории, то переставить его в новую
    user_dao: Optional[UserDao] = await user_repository.get_first_by_column(UserDao.user_id, user_id)
    if user_dao is None:
        user_dao = UserDao(user_id=user_id, auditorium_id=user_short_dto.auditorium_id,
                           silent_status=user_short_dto.silent_status, end_of_location=end_of_location_dt)
        await user_repository.add(user_dao)
    else:
        user_dao.auditorium_id = user_short_dto.auditorium_id
        user_dao.silent_status = user_short_dto.silent_status
        user_dao.end_of_location = end_of_location_dt
        await user_repository.update(user_dao)

    try:
        await send_notification_about_user_in_auditorium(user_dao, auditorium)
    except Exception as e:
        logging.error(f"Error while sending notification about user in auditorium: {e}")

    try:
        user_dto: UserAuditoriumDto = UserAuditoriumDto(user_id=user_dao.user_id, auditorium=auditorium,
                                                        silent_status=user_dao.silent_status,
                                                        end=end_of_location)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=f"User {user_id} not found")
    return user_dto


@router.delete("/remove_user",
               responses={200: {"description": "OK", "model": UserAuditoriumDeleteResponseDto},
                          409: {"description": "User not in auditorium", "model": DefaultResponse},
                          404: {"description": "User/Classroom not found", "model": AuditoriumUserErrorResponse}},
               description="Remove user from auditorium", summary="Remove user from auditorium")
async def remove_user_from_auditorium(user_id: int = Header(alias=to_camel("user_id")),
                                      user_repository: GenericRepository = Depends(get_user_repository)
                                      ) -> Any:
    logging.info(user_id)
    user_dao: Optional[UserDao] = await user_repository.get_first_by_column(UserDao.user_id, user_id)
    if user_dao is None:
        aud_user_response: AuditoriumUserErrorResponse = AuditoriumUserErrorResponse(message="User not in auditorium",
                                                                                     status_code=409,
                                                                                     user_not_found=True,
                                                                                     auditorium_not_found=False)
        return JSONResponse(status_code=404, content=aud_user_response.model_dump(mode='json', by_alias=True))

    auditorium_id = user_dao.auditorium_id
    auditorium: Optional[AuditoriumDto] = await hse_api_client.get_auditorium_by_id(auditorium_id)
    if auditorium is None:
        aud_user_response: AuditoriumUserErrorResponse = AuditoriumUserErrorResponse(message="Auditorium not found",
                                                                                     status_code=404,
                                                                                     user_not_found=False,
                                                                                     auditorium_not_found=True)
        return JSONResponse(status_code=404, content=aud_user_response.model_dump(mode='json', by_alias=True))

    await user_repository.delete(user_dao)

    return UserAuditoriumDeleteResponseDto(user_id=user_id, auditorium=auditorium)
