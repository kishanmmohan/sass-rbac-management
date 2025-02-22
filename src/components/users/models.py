from sqlalchemy import Boolean, Column, Integer, String, UniqueConstraint

from src.core.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)

    # add unique constraint to user
    __table_args__ = (
        UniqueConstraint("username"),
    )

    def __repr__(self):
        return f"<User {self.username}>"
