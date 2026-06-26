from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.roles.schemas import RoleCreate, RoleResponse, RoleUpdate
from app.core.database import get_db
from app.domains.auth.dependencies import get_current_active_user
from app.domains.roles.dependencies import RoleChecker
from app.domains.roles.service import RoleService

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("", response_model=List[RoleResponse])
async def list_roles(
    db: AsyncSession = Depends(get_db),  # noqa: B008
    current_user=Depends(get_current_active_user),  # noqa: B008
    _=Depends(RoleChecker(["roles:read"])),  # noqa: B008
):
    return await RoleService.get_all_roles(db)


@router.post("", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_in: RoleCreate,
    db: AsyncSession = Depends(get_db),  # noqa: B008
    current_user=Depends(get_current_active_user),  # noqa: B008
    _=Depends(RoleChecker(["roles:create"])),  # noqa: B008
):
    return await RoleService.create_role(db, role_in.model_dump())


@router.get("/{role_id}", response_model=RoleResponse)
async def get_role(
    role_id: int,
    db: AsyncSession = Depends(get_db),  # noqa: B008
    current_user=Depends(get_current_active_user),  # noqa: B008
    _=Depends(RoleChecker(["roles:read"])),  # noqa: B008
):
    return await RoleService.get_role(db, role_id)


@router.put("/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: int,
    role_in: RoleUpdate,
    db: AsyncSession = Depends(get_db),  # noqa: B008
    current_user=Depends(get_current_active_user),  # noqa: B008
    _=Depends(RoleChecker(["roles:update"])),  # noqa: B008
):
    update_data = role_in.model_dump(exclude_unset=True)
    return await RoleService.update_role(db, role_id, update_data)


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    role_id: int,
    db: AsyncSession = Depends(get_db),  # noqa: B008
    current_user=Depends(get_current_active_user),  # noqa: B008
    _=Depends(RoleChecker(["roles:delete"])),  # noqa: B008
):
    await RoleService.delete_role(db, role_id)
