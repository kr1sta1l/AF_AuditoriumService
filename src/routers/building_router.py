from fastapi import APIRouter, Query, Header, HTTPException, Depends

from fastapi import APIRouter, Query
from typing import Union, Dict, List, Any, Optional
from fastapi.responses import JSONResponse
from src.hse_api_client import hse_api_client
from pydantic.alias_generators import to_camel

from src.modules.dto.auditoriums.auditorium_short_dto import AuditoriumShortDto
from src.modules.dto.buildings.building_auditoriums_dto import BuildingAuditoriumsDto
from src.modules.dto.buildings.building_dto import BuildingDto

router = APIRouter()


@router.get("", description="Get list of buildings. Included in headers: "
                            "pages_amount - amount of pages, "
                            "entities_amount - amount of entities in response.",
            summary="Get list of buildings",
            responses={200: {"description": "OK", "model": List[BuildingDto]}},
            response_model=List[BuildingDto])
async def get_buildings(language: str = Query("ru"),
                        page: int = Query(ge=0, default=0, alias=to_camel("page")),
                        size: int = Query(ge=1, le=100, default=50, alias=to_camel("size"))) -> Any:
    page += 1
    list_of_buildings: Dict[str, List[BuildingDto] | int] = \
        await hse_api_client.get_buildings(page=page, page_size=size, language=language)

    headers = {"entities_amount": str(list_of_buildings["buildings_amount"]),
               "pages_amount": str(list_of_buildings["pages_amount"])}
    result: List[Union[BuildingDto, Dict]] = list_of_buildings["buildings"]
    for i, el in enumerate(result):
        result[i] = el.model_dump(by_alias=True)

    return JSONResponse(headers=headers, content=result, media_type="application/json")


@router.get("/{building_id}", description="Get building by id", summary="Get building by id",
            responses={200: {"description": "OK"}, 404: {"description": "Building not found", "model": BuildingDto}})
async def get_building(building_id: int, language: str = Query("ru", alias=to_camel("language"))) -> BuildingDto:
    building: BuildingDto = await hse_api_client.get_building_by_id(building_id, language=language)
    return building


# @router.get("/building/{building_id}/auditoriums", description="Search building by name",
#             summary="Search building by name",
#             responses={200: {"description": "OK", "model": List[BuildingDto]},
#                        404: {"description": "Building not found", "model": BuildingDto}},
#             response_model=List[BuildingDto])
# async def get_building_auditoriums(building_id: int, language_code: str = Query("ru",
#                                                                                 alias=to_camel("language_code")),
#                                    page: int = Query(ge=0, default=0, alias=to_camel("page")),
#                                    size: int = Query(ge=1, le=100, default=10, alias=to_camel("size"))
#                                    ) -> BuildingAuditoriumsDto:
#     building: BuildingDto = await hse_api_client.get_building_by_id(building_id, language=language_code)
#     if building is None:
#         raise HTTPException(status_code=404, detail=f"Building {building_id} not found")
#     auditoriums: List[AuditoriumShortDto] = await hse_api_client.get_auditoriums_in_building(building,
#                                                                                              language=language_code)
#     result: BuildingAuditoriumsDto = BuildingAuditoriumsDto(building=building, auditoriums=auditoriums)
#
#     return result
