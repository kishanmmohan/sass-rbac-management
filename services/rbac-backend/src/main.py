from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.db import init_db
from core.middlewares.logging import LoggingMiddleware


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Ensure the database and tables are created when the app starts
    await init_db()
    yield


def create_application() -> FastAPI:
    from components import health, users

    application = FastAPI(lifespan=lifespan)

    application.include_router(health.router)
    application.include_router(users.router, prefix="/users", tags=["users"])

    return application


app = create_application()

app.add_middleware(LoggingMiddleware)  # noqa
