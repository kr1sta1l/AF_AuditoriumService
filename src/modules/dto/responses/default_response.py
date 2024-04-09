from src.modules.dto.base_dto import BaseDto


class DefaultResponse(BaseDto):
    message: str
    status_code: int
