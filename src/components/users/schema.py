from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

from .enums import UserTypeEnum
from ...core import BaseResponse


class UserShortSchema(BaseModel):
    id: int
    auth0_id: str
    name: str
    email: EmailStr
    is_active: bool


class UserDetailSchema(UserShortSchema):
    auth0_id: str
    name: str
    email: str
    is_active: bool
    user_type: UserTypeEnum
    created_at: datetime
    updated_at: Optional[datetime]


class UserCreateSchema(BaseModel):
    name: str
    email: EmailStr
    auth0_id: str
    user_type: UserTypeEnum = UserTypeEnum.ORG_USER


class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    user_type: Optional[UserTypeEnum] = None
    is_active: Optional[bool] = None


class UserCreateResponseSchema(BaseResponse):
    data: UserDetailSchema
