from typing import List, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from .models import User


class UserRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_user(self, name: str, email: str, auth0_id: str, user_type: str, is_active: bool = True) -> User:
        user_obj = User(name=name, email=email, auth0_id=auth0_id, user_type=user_type, is_active=is_active)
        self.db_session.add(user_obj)
        self.db_session.commit()
        self.db_session.refresh(user_obj)
        return user_obj

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.db_session.get(User, user_id)

    def get_all_users(self, search_query: Optional[str] = None, limit: int = 10, offset: int = 0,
                      sort_by: Optional[str] = None, sort_order: str = 'asc') -> List[User]:
        query = self.db_session.query(User)
        if search_query:
            query = query.filter(or_(User.name.ilike(f"%{search_query}%"), User.email.ilike(f"%{search_query}%")))
        if sort_by:
            query = query.order_by(
                getattr(User, sort_by).desc() if sort_order == 'desc' else getattr(User, sort_by).asc())
        else:
            query = query.order_by(User.id)
        return query.offset(offset).limit(limit).all()  # noqa

    def update_user(self, user_id: int, **kwargs) -> Optional[User]:
        user = self.get_user_by_id(user_id)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            self.db_session.commit()
            self.db_session.refresh(user)
        return user

    def delete_user(self, user_id: int) -> bool:
        """Permanently delete a user from the database."""
        user = self.get_user_by_id(user_id)
        if user:
            self.update_user(user_id, is_active=False)

            return True
        return False
