from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    RoleAlreadyExistsError,
    RoleNotFoundError,
    SystemRoleDeleteError,
)
from app.domains.roles.models import Role
from app.repositories import role as repository


class RoleService:
    @staticmethod
    async def get_all_roles(session: AsyncSession) -> list[Role]:
        return await repository.get_all_roles(session)

    @staticmethod
    async def get_role(session: AsyncSession, role_id: int) -> Role:
        role = await repository.get_role_by_id(session, role_id)
        if not role:
            raise RoleNotFoundError()
        return role

    @staticmethod
    async def create_role(session: AsyncSession, create_data: dict) -> Role:
        """Take the dictionary and db session as a parameter and pass the context."""
        existing = await repository.get_role_by_name(session, create_data.get("name"))
        if existing:
            raise RoleAlreadyExistsError()

        role = Role(**create_data)
        role = await repository.create_role(session, role)
        await session.commit()
        return role

    @staticmethod
    async def update_role(session: AsyncSession, role_id: int, update_data: dict) -> Role:
        role = await RoleService.get_role(session, role_id)

        if "name" in update_data and update_data["name"] != role.name:
            existing = await repository.get_role_by_name(session, update_data["name"])
            if existing:
                raise RoleAlreadyExistsError(message="Role name already in use")

        role = await repository.update_role(session, role, update_data)
        await session.commit()
        return role

    @staticmethod
    async def delete_role(session: AsyncSession, role_id: int) -> None:
        role = await RoleService.get_role(session, role_id)
        if role.name in ["admin", "user"]:
            raise SystemRoleDeleteError()

        await repository.delete_role(session, role)
        await session.commit()
