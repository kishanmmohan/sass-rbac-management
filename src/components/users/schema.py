from pydantic import BaseModel

from .models import UserTypeEnum


class UserBase(BaseModel):
    name: str
    email: str
    auth0_id: str
    is_active: bool = True
    user_type: UserTypeEnum = UserTypeEnum.STAFF


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    name: str
    email: str
    auth0_id: str
    is_active: bool
    user_type: UserTypeEnum


class UserUpdate(UserBase):
    name: str
    email: str
    is_active: bool
    user_type: UserTypeEnum
