from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from components.users.repository import UserRepository
from components.users.schema import CreateUserRequest, UpdateUserRequest, UserDetail, UserShort
from components.users.service import UserService
from core.db import get_db

router = APIRouter()


# Dependency to get UserService
def get_user_service(_: Request, db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository(db)
    return UserService(user_repo)


@router.post("/", response_model=UserDetail, status_code=201)
async def create_user(user: CreateUserRequest, user_service: UserService = Depends(get_user_service)):
    user_data = await user_service.create_user(user)
    return user_data


@router.get("/{user_id}", response_model=UserDetail, status_code=200)
async def get_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    user_data = await user_service.get_user_by_id(user_id)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    return user_data


@router.get("/", response_model=List[UserShort], status_code=200)
async def get_users(
        search_query: Optional[str] = Query(None, description="Search users by name or email"),
        limit: int = Query(10, description="Number of users per page"),
        offset: int = Query(0, description="Offset for pagination"),
        sort_by: Optional[str] = Query(None, description="Field to sort by"),
        sort_order: str = Query("asc", description="Sort order: 'asc' or 'desc'"),
        user_service: UserService = Depends(get_user_service)
):
    users = await user_service.get_all_users(search_query, limit, offset, sort_by, sort_order)
    return users


@router.patch("/{user_id}", response_model=UserDetail, status_code=200)
async def update_user(user_id: int, update_data: UpdateUserRequest,
                      user_service: UserService = Depends(get_user_service)):
    updated_user = await user_service.update_user(user_id, update_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete("/{user_id}")
async def delete_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    deleted = await user_service.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(content="User deleted successfully", status_code=200)
