from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domains.roles.models import Role


async def get_role_by_name(session: AsyncSession, role_name: str) -> Role | None:
    result = await session.execute(select(Role).options(selectinload(Role.permissions)).where(Role.name == role_name))
    return result.scalar_one_or_none()


async def create_role(session: AsyncSession, role: Role) -> Role:
    session.add(role)
    await session.flush()
    return role


async def update_role(session: AsyncSession, role: Role, update_data: dict) -> Role:
    for key, value in update_data.items():
        setattr(role, key, value)
    session.add(role)
    await session.flush()
    return role


async def delete_role(session: AsyncSession, role: Role) -> None:
    await session.delete(role)
    await session.flush()


async def get_role_by_id(session: AsyncSession, role_id: int) -> Role | None:
    result = await session.execute(select(Role).options(selectinload(Role.permissions)).where(Role.id == role_id))
    return result.scalar_one_or_none()


async def get_all_roles(session: AsyncSession) -> list[Role]:
    result = await session.execute(select(Role).options(selectinload(Role.permissions)))
    return list(result.scalars().all())
