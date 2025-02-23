from .repository import UserRepository
from .schema import UserCreate


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user(self, user_id: int):
        return self.user_repository.get_user(user_id)

    def create_user(self, user: UserCreate):
        return self.user_repository.create_user(user)

    def get_users(self, skip: int = 0, limit: int = 100):
        return self.user_repository.get_users(skip, limit)