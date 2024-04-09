import json
import asyncio
import logging
import aio_pika
from src.config import config
from src.modules.dao import UserDao
from src.controllers.session import get_user_repository, get_rabbit_url


async def start_jobber() -> None:
    logging.info("Jobber started")
    url = get_rabbit_url(config.RB_USERNAME, config.RB_PASSWORD, config.RB_CONNECTION_HOST,
                         config.RB_CONNECTION_PORT, config.RB_VIRTUAL_HOST)
    connection = await aio_pika.connect_robust(url=url)

    queue_name = config.LISTEN_QUEUE

    async with connection:
        channel = await connection.channel()

        await channel.set_qos(prefetch_count=10)

        queue = await channel.declare_queue(queue_name, auto_delete=False, durable=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    logging.warning(message.body)
                    try:
                        body_dict = json.loads(message.body.decode())
                    except json.JSONDecodeError:
                        logging.error("Message is not a json")
                        continue
                    try:
                        user_id = body_dict['userid']
                    except KeyError:
                        logging.error("User id was not found in message")
                        continue

                    user_repository = get_user_repository()
                    user_dao: UserDao = await user_repository.get_one_by_whereclause(UserDao.user_id == user_id)
                    if user_dao is not None:
                        await user_repository.delete(user_dao)
                        logging.info(f"User with id {user_id} was deleted")
                    else:
                        logging.warning(f"User with id {user_id} was not found")
    logging.warning("Jobber finished")


if __name__ == "__main__":
    asyncio.run(start_jobber())
