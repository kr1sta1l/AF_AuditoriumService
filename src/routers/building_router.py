from fastapi import APIRouter, Query
from typing import Union, Dict, List, Any
from fastapi.responses import JSONResponse
from src.hse_api_client import hse_api_client
from pydantic.alias_generators import to_camel
from src.modules.dto.buildings.building_dto import BuildingDto

router = APIRouter()


@router.get("", description="Get list of buildings. Included in headers: "
                            "pages_amount - amount of pages, "
                            "entities_amount - amount of entities in response.",
            summary="Get list of buildings",
            responses={200: {"description": "OK", "model": List[BuildingDto]}},
            response_model=List[BuildingDto])
async def get_buildings(language_code: str = Query("ru", alias=to_camel("language_code")),
                        page: int = Query(ge=0, default=0, alias=to_camel("page")),
                        size: int = Query(ge=1, le=100, default=50, alias=to_camel("size"))) -> Any:
    page += 1
    list_of_buildings: Dict[str, List[BuildingDto] | int] = \
        await hse_api_client.get_buildings(page=page, page_size=size, language=language_code)

    headers = {"entities_amount": str(list_of_buildings["buildings_amount"]),
               "pages_amount": str(list_of_buildings["pages_amount"]),
               "Access-Control-Expose-Headers": "*"}
    result: List[Union[BuildingDto, Dict]] = list_of_buildings["buildings"]
    for i, el in enumerate(result):
        result[i] = el.model_dump(by_alias=True)

    return JSONResponse(headers=headers, content=result, media_type="application/json")


@router.get("/{building_id}", description="Get building by id", summary="Get building by id",
            responses={200: {"description": "OK"}, 404: {"description": "Building not found", "model": BuildingDto}})
async def get_building(building_id: int, language_code: str = Query("ru", alias=to_camel("language_code"))) -> BuildingDto:
    building: BuildingDto = await hse_api_client.get_building_by_id(building_id, language=language_code)
    return building
