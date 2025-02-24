from .repository import UserRepository
from .schema import UserCreateSchema, UserDetailSchema


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user(self, user_id: int):
        return self.user_repository.get_user_by_id(user_id)

    def create_user(self, user: UserCreateSchema) -> UserDetailSchema:
        user_obj = self.user_repository.create_user(
            user.name,
            str(user.email),
            user.auth0_id,
            user.user_type.name,
        )
        return UserDetailSchema(
            id=user_obj.id,
            name=user_obj.name,
            email=user_obj.email,
            auth0_id=user_obj.auth0_id,
            is_active=user_obj.is_active,
            user_type=user_obj.user_type,
            created_at=user_obj.created_at,
            updated_at=user_obj.updated_at
        )
