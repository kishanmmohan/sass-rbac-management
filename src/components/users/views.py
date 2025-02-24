from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from mypy.dmypy.client import request
from sqlalchemy.orm import Session

from src.core.db import get_db

from .repository import UserRepository
from .schema import UserCreateSchema, UserCreateResponseSchema
from .service import UserService

router = APIRouter()


# Dependency to get UserService
def get_user_service(_: Request, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    return UserService(user_repo)


@router.post("/", response_model=UserCreateResponseSchema, status_code=201)
def create_user(user: UserCreateSchema, user_service: UserService = Depends(get_user_service)):
    user_data = user_service.create_user(user)

    return UserCreateResponseSchema(message="Created", data=user_data, code=100)
