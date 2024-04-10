from src.config import config
from contextlib import asynccontextmanager
from src.controllers.session import init_db

import random
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.exceptions.exceptions import exception_handler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.jobber.delete_users_associations import start_jobber
from routers import auditorium_router, building_router, technical_router
from src.routers.health_checks_routes import readiness_router, liveness_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Application started")
    logging.basicConfig(level=config.logging_level_strint_to_int(config.AS_LOG_LEVEL),
                        format="%(asctime)s - %(levelname)s - %(message)s")
    random.seed(42)
    await init_db()

    scheduler = AsyncIOScheduler()
    scheduler.add_job(start_jobber, 'interval', seconds=10)
    scheduler.start()

    yield

    scheduler.shutdown()
    logging.info("Application stopped")


def configure_app(app: FastAPI):
    app.include_router(auditorium_router.router, prefix="/auditorium", tags=["Auditorium"])
    app.include_router(building_router.router, prefix="/buildings", tags=["Building"])
    app.include_router(technical_router.router, tags=["Technical"])
    app.include_router(readiness_router, prefix="/health")
    app.include_router(liveness_router, prefix="/health")

    app.exception_handler(400)(exception_handler)
    app.exception_handler(404)(exception_handler)
    app.exception_handler(409)(exception_handler)
    app.exception_handler(503)(exception_handler)

    origins = [
        "*"
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


if __name__ == "__main__":
    import uvicorn

    app: FastAPI = FastAPI(title="Auditorium service", lifespan=lifespan)
    configure_app(app)

    # uvicorn_logger = logging.getLogger("uvicorn")
    # uvicorn_logger.handlers[0].setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    uvicorn.run(app, host=config.AS_HOST, port=config.AS_PORT)
