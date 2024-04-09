import json
import asyncio
import logging
import aio_pika
from src.config import config
from src.modules.dao import UserDao
from src.controllers.session import get_user_repository


async def start_jobber() -> None:
    logging.info("Jobber started")
    connection = await aio_pika.connect_robust(
        host=config.RB_CONNECTION_HOST,
        port=config.RB_CONNECTION_PORT
    )

    queue_name = config.LISTEN_QUEUE

    async with connection:
        # Creating channel
        channel = await connection.channel()

        # Will take no more than 10 messages in advance
        await channel.set_qos(prefetch_count=10)

        # Declaring queue
        queue = await channel.declare_queue(queue_name, auto_delete=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    logging.warning(message.body)
                    body_dict = json.loads(message.body.decode())
                    user_id = body_dict['userid']

                    user_repository = get_user_repository()
                    user_dao: UserDao = await user_repository.get_one_by_whereclause(UserDao.user_id == user_id)
                    if user_dao is not None:
                        await user_repository.delete(user_dao)
                        logging.info(f"User with id {user_id} was deleted")
    logging.warning("Jobber finished")


if __name__ == "__main__":
    asyncio.run(start_jobber())
