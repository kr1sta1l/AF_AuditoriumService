from .default_response import DefaultResponse


class AuditoriumUserErrorResponse(DefaultResponse):
    user_not_found: bool
    auditorium_not_found: bool
