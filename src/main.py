import os
from pathlib import Path
from src.config import config
from contextlib import asynccontextmanager
from src.controllers.session import init_db


directory = Path(os.path.dirname(os.path.abspath(__file__)))
config.load_env(directory / ".env")

import random
import logging
from fastapi import FastAPI
from starlette.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from routers import auditorium_router, building_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Application started")
    logging.basicConfig(level=config.AS_LOG_LEVEL, format="%(asctime)s - %(levelname)s - %(message)s")
    random.seed(42)
    await init_db()
    yield
    logging.info("Application stopped")


app: FastAPI = FastAPI(title="Auditorium service", lifespan=lifespan)
app.include_router(auditorium_router.router, prefix="/auditorium", tags=["Auditorium"])
app.include_router(building_router.router, prefix="/buildings", tags=["Building"])

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


@app.exception_handler(400)
async def validation_exception_handler(request, exc):
    return JSONResponse(status_code=400, content={"message": exc.detail})


@app.exception_handler(404)
async def validation_exception_handler(request, exc):
    return JSONResponse(status_code=404, content={"message": exc.detail})


@app.get("/openapi.json", include_in_schema=False)
async def get_openapi_endpoint():
    return JSONResponse(content=get_openapi(title="docs", version="0.1.0", routes=app.routes))


if __name__ == "__main__":
    import uvicorn
    # uvicorn_logger = logging.getLogger("uvicorn")
    # uvicorn_logger.handlers[0].setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    uvicorn.run(app, host=config.AS_HOST, port=config.AS_PORT)
