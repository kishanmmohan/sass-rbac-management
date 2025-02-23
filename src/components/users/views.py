from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.db import get_db

from .repository import UserRepository
from .schema import User, UserCreate
from .service import UserService

router = APIRouter()


# Dependency to get UserService
def get_user_service(db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    return UserService(user_repo)


@router.post("/", response_model=User, status_code=201)
def create_user(user: UserCreate, user_service: UserService = Depends(get_user_service)):
    return user_service.create_user(user)


@router.get("/", response_model=List[User], status_code=200)
def read_users(skip: int = 0, limit: int = 100, user_service: UserService = Depends(get_user_service)):
    if skip < 0 or limit <= 0:
        raise HTTPException(status_code=422, detail="Invalid pagination parameters")
    return user_service.get_users(skip, limit)


@router.get("/{user_id}", response_model=User, status_code=200)
def read_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    db_user = user_service.get_user(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
