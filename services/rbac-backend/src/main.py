import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.db import init_db

logger = logging.getLogger("uvicorn")


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("Starting up...")
    # Ensure the database and tables are created when the app starts
    init_db()
    yield
    logger.info("Shutting down...")


def create_application() -> FastAPI:
    from components import health, users

    application = FastAPI(lifespan=lifespan)

    application.include_router(health.router)
    application.include_router(users.router, prefix="/users", tags=["users"])

    return application


app = create_application()
