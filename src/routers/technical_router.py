from fastapi import APIRouter, HTTPException
from src.utils.technical_utils import database_connection_successful
from src.modules.dto.responses.default_response import DefaultResponse
from src.modules.dto.responses.short_default_response import ShortDefaultResponse

router = APIRouter()


@router.get("/health", responses={200: {"description": "OK",
                                        "model": ShortDefaultResponse}},
            response_model=ShortDefaultResponse)
async def health_check():
    return ShortDefaultResponse(message="OK")


@router.get("/readiness", responses={200: {"description": "OK",
                                           "model": ShortDefaultResponse},
                                     503: {"description": "Service unavailable",
                                           "model": ShortDefaultResponse}},
            response_model=ShortDefaultResponse)
async def readiness_check():
    if database_connection_successful():
        return ShortDefaultResponse(message="OK")
    else:
        raise HTTPException(status_code=503, detail="Service unavailable")
