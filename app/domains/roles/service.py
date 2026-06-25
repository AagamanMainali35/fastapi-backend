from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AppException
from app.domains.roles import repository
from app.domains.roles.models import Role


class RoleService:
    @staticmethod
    async def get_all_roles(session: AsyncSession) -> list[Role]:
        return await repository.get_all_roles(session)

    @staticmethod
    async def get_role(session: AsyncSession, role_id: int) -> Role:
        role = await repository.get_role_by_id(session, role_id)
        if not role:
            raise AppException(message="Role not found", code=404)
        return role

    @staticmethod
    async def create_role(session: AsyncSession, create_data: dict) -> Role:
        existing = await repository.get_role_by_name(session, create_data.get("name"))
        if existing:
            raise AppException(message="Role already exists", code=400)

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
                raise AppException(message="Role name already in use", code=400)

        role = await repository.update_role(session, role, update_data)
        await session.commit()
        return role

    @staticmethod
    async def delete_role(session: AsyncSession, role_id: int) -> None:
        role = await RoleService.get_role(session, role_id)
        if role.name in ["admin", "user"]:
            raise AppException(message="Cannot delete system roles", code=400)

        await repository.delete_role(session, role)
        await session.commit()
