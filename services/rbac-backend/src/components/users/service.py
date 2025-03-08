from typing import List, Optional

from core.middlewares.logging import get_logger, log_method

from .repository import UserRepository
from .schema import CreateUserRequest, UpdateUserRequest, UserDetail, UserShort


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.logging = get_logger(self.__class__.__name__)

    async def get_user(self, user_id: int):
        return await self.user_repository.get_user_by_id(user_id)

    async def create_user(self, user: CreateUserRequest) -> UserDetail:
        user_obj = await self.user_repository.create_user(
            user.name,
            str(user.email),
            user.auth0_id,
            user.user_type.name,
        )
        return UserDetail(
            id=user_obj.id,
            name=user_obj.name,
            email=user_obj.email,
            auth0_id=user_obj.auth0_id,
            is_active=user_obj.is_active,
            user_type=user_obj.user_type,
            created_at=user_obj.created_at,
            updated_at=user_obj.updated_at
        )

    @log_method()
    async def get_user_by_id(self, user_id: int) -> Optional[UserDetail]:
        """Fetch a user by ID."""
        user = await self.user_repository.get_user_by_id(user_id)
        self.logging.info(f'User Service result: {user.name}')
        if user:
            return UserDetail(
                id=user.id,
                name=user.name,
                email=user.email,  # noqa
                auth0_id=user.auth0_id,
                user_type=user.user_type,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
        return None

    async def get_all_users(self, search_query: Optional[str] = None, limit: int = 10, offset: int = 0,
                            sort_by: Optional[str] = None, sort_order: str = 'asc') -> List[UserShort]:
        """Fetch a list of users with pagination and sorting."""
        users = await self.user_repository.get_all_users(
            search_query=search_query, limit=limit, offset=offset, sort_by=sort_by, sort_order=sort_order
        )
        return [
            UserShort(
                id=user.id,
                auth0_id=user.auth0_id,
                name=user.name,
                email=user.email,  # noqa
                is_active=user.is_active
            ) for user in users
        ]

    async def update_user(self, user_id: int, update_data: UpdateUserRequest) -> Optional[UserDetail]:
        """Update user details."""
        updated_user = await self.user_repository.update_user(user_id, **update_data.model_dump(exclude_unset=True))
        if updated_user:
            return UserDetail(
                id=updated_user.id,
                auth0_id=updated_user.auth0_id,
                name=updated_user.name,
                email=updated_user.email,
                is_active=updated_user.is_active,
                user_type=updated_user.user_type,
                created_at=updated_user.created_at,
                updated_at=updated_user.updated_at
            )
        return None

    async def delete_user(self, user_id: int) -> bool:
        return await self.user_repository.delete_user(user_id)
