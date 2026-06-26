from typing import List

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.domains.auth.dependencies import get_current_active_user
from app.domains.auth.models import User
from app.domains.roles.models import Role


class RoleChecker:
    """Dependency class to check if the current user has the required permissions."""

    def __init__(self, required_permissions: List[str]):
        self.required_permissions = required_permissions

    async def __call__(
        self,
        current_user: User = Depends(get_current_active_user),  # noqa: B008
        db: AsyncSession = Depends(get_db),  # noqa: B008
    ):
        if not current_user.role_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User has no role assigned."
            )

        result = await db.execute(
            select(Role)
            .options(selectinload(Role.permissions))
            .where(Role.id == current_user.role_id)
        )
        role = result.scalar_one_or_none()

        if not role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Role not found."
            )

        user_permission_names = [p.name for p in role.permissions]

        for required_perm in self.required_permissions:
            if required_perm not in user_permission_names:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Missing required permission: {required_perm}"
                )
