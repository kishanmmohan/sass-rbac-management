from typing import List, Optional

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User


class UserRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, name: str, email: str, auth0_id: str, user_type: str, is_active: bool = True) -> User:
        user_obj = User(name=name, email=email, auth0_id=auth0_id, user_type=user_type, is_active=is_active)
        self.db_session.add(user_obj)
        await self.db_session.commit()
        await self.db_session.refresh(user_obj)
        return user_obj

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        result = await self.db_session.get(User, user_id)
        return result

    async def get_all_users(
            self, search_query: Optional[str] = None, limit: int = 10, offset: int = 0,
            sort_by: Optional[str] = None, sort_order: str = 'asc'
    ) -> List[User]:
        stmt = select(User)

        if search_query:
            stmt = stmt.where(or_(User.name.ilike(f"%{search_query}%"), User.email.ilike(f"%{search_query}%")))

        if sort_by:
            stmt = stmt.order_by(
                getattr(User, sort_by).desc() if sort_order == 'desc' else getattr(User, sort_by).asc()
            )
        else:
            stmt = stmt.order_by(User.id)

        stmt = stmt.offset(offset).limit(limit)

        result = await self.db_session.execute(stmt)
        return list(result.scalars().all())

    async def update_user(self, user_id: int, **kwargs) -> Optional[User]:
        user = await self.get_user_by_id(user_id)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            await self.db_session.commit()
            await self.db_session.refresh(user)
        return user

    async def delete_user(self, user_id: int) -> bool:
        user = await self.get_user_by_id(user_id)
        if user:
            await self.update_user(user_id, is_active=False)
            return True
        return False
