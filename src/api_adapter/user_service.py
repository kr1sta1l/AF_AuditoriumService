import logging

import httpx
from src.config import config


class UserServiceClient:
    def __init__(self):
        pass

    @staticmethod
    async def is_user_exits(user_id: int) -> bool:
        async with httpx.AsyncClient() as client:
            try:
                headers = {
                    "userid": str(user_id)
                }
                response = await client.get(f"{config.USER_SERVICE_HOST}:{config.USER_SERVICE_PORT}/profile",
                                            headers=headers)
                logging.warning(f"{response.status_code}: {response.text}")
            except Exception:
                return False
            if response.status_code == 200:
                return True
            return False
