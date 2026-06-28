from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.users.schema import UserCreateModel, UserResponseModel, UserUpdateModel
from app.core.database import get_db
from app.domains.auth.dependencies import get_current_active_user
from app.domains.roles.dependencies import RoleChecker
from app.domains.users.service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[UserResponseModel])
async def list_users(
    db: AsyncSession = Depends(get_db),  # noqa: B008
    current_user=Depends(get_current_active_user),  # noqa: B008
    _=Depends(RoleChecker(["users:read"])),  # noqa: B008
):
    return await UserService.get_all_users(db)


@router.get("/{user_id}", response_model=UserResponseModel)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),  # noqa: B008
    current_user=Depends(get_current_active_user),  # noqa: B008
    _=Depends(RoleChecker(["users:read"])),  # noqa: B008
):
    return await UserService.get_user(db, user_id)


@router.post("", response_model=UserResponseModel, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreateModel,
    db: AsyncSession = Depends(get_db),  # noqa: B008
    current_user=Depends(get_current_active_user),  # noqa: B008
    _=Depends(RoleChecker(["users:create"])),  # noqa: B008
):
    return await UserService.create_user(db, user_in.model_dump())


@router.patch("/{user_id}", response_model=UserResponseModel)
async def update_user(
    user_id: int,
    user_in: UserUpdateModel,
    db: AsyncSession = Depends(get_db),  # noqa: B008
    current_user=Depends(get_current_active_user),  # noqa: B008
    _=Depends(RoleChecker(["users:update"])),  # noqa: B008
):
    update_data = user_in.model_dump(exclude_unset=True)
    return await UserService.update_user(db, user_id, update_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),  # noqa: B008
    current_user=Depends(get_current_active_user),  # noqa: B008
    _=Depends(RoleChecker(["users:delete"])),  # noqa: B008
):
    await UserService.delete_user(db, user_id)
