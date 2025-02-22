from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
    is_active: bool = True


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class User(UserBase):
    id: int
    username: str
    email: str
