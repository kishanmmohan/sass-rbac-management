from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

from .enums import UserTypeEnum


class UserShort(BaseModel):
    id: int
    auth0_id: str
    name: str
    email: EmailStr
    is_active: bool


class UserDetail(UserShort):
    auth0_id: str
    name: str
    email: str
    is_active: bool
    user_type: UserTypeEnum
    created_at: datetime
    updated_at: Optional[datetime]


class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    auth0_id: str
    user_type: UserTypeEnum = UserTypeEnum.ORG_USER


class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    user_type: Optional[UserTypeEnum] = None
    is_active: Optional[bool] = None
