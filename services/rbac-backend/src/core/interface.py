from .middlewares.logging import get_logger
from sqlalchemy.ext.asyncio import AsyncSession


class BaseService:
    def __init__(self):
        self.logging = get_logger(self.__class__.__name__)


class BaseRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.logging = get_logger(self.__class__.__name__)
