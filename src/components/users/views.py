from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Query, Response

from sqlalchemy.orm import Session

from src.core.db import get_db

from .repository import UserRepository
from .schema import CreateUserRequest, UpdateUserRequest, UserShort, UserDetail
from .service import UserService

router = APIRouter()


# Dependency to get UserService
def get_user_service(_: Request, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    return UserService(user_repo)


@router.post("/", response_model=UserDetail, status_code=201)
def create_user(user: CreateUserRequest, user_service: UserService = Depends(get_user_service)):
    user_data = user_service.create_user(user)
    return user_data


@router.get("/{user_id}", response_model=UserDetail, status_code=200)
def get_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    user_data = user_service.get_user_by_id(user_id)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    return user_data


@router.get("/", response_model=List[UserShort], status_code=200)
def get_users(
        search_query: Optional[str] = Query(None, description="Search users by name or email"),
        limit: int = Query(10, description="Number of users per page"),
        offset: int = Query(0, description="Offset for pagination"),
        sort_by: Optional[str] = Query(None, description="Field to sort by"),
        sort_order: str = Query("asc", description="Sort order: 'asc' or 'desc'"),
        user_service: UserService = Depends(get_user_service)
):
    users = user_service.get_all_users(search_query, limit, offset, sort_by, sort_order)
    return users


@router.patch("/{user_id}", response_model=UserDetail, status_code=200)
def update_user(user_id: int, update_data: UpdateUserRequest, user_service: UserService = Depends(get_user_service)):
    updated_user = user_service.update_user(user_id, update_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete("/{user_id}")
def delete_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    deleted = user_service.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(content="User deleted successfully", status_code=200)
