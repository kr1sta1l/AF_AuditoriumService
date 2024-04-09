import json
import logging
import aio_pika
from src.config import config
from src.modules.dao import UserDao
from src.modules.dto.auditoriums.auditorium_dto import AuditoriumDto
from src.modules.dto.auditoriums.auditorium_short_building_dto import AuditoriumShortBuildingDto


async def send_notification_about_user_in_auditorium(user_dao: UserDao, auditorium_dto: AuditoriumDto) -> None:
    auditorium_short_building_dto: AuditoriumShortBuildingDto = AuditoriumShortBuildingDto.from_dto(
        auditorium_dto)

    notification = {
        'auditorium': auditorium_short_building_dto.model_dump(),
        'user': {
            "id": user_dao.id,
            "silentStatus": user_dao.silent_status,
            "end": user_dao.end_of_location
        }
    }
    logging.warning(f"notification: {notification}")

    try:
        async with aio_pika.connect_robust(config.RB_CONNECTION_HOST) as connection:
            try:
                async with connection.channel() as channel:
                    try:
                        await channel.default_exchange.publish(
                            aio_pika.Message(body=json.dumps(notification).encode()),
                            routing_key=config.SEND_QUEUE
                        )
                    except Exception as e:
                        logging.error(f"Error while sending notification: {e}")
            except Exception as e:
                logging.error(f"Error while getting channel: {e}")
    except Exception as e:
        logging.error(f"Error while connecting to rabbitmq: {e}")
