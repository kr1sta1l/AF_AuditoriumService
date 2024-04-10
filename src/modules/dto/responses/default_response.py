from src.modules.dto.base_dto import BaseDto
from .short_default_response import ShortDefaultResponse


class DefaultResponse(ShortDefaultResponse):
    status_code: int
