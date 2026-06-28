from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.roles.models import Role
from app.domains.users.models import User
from app.repositories import base
from app.repositories.role import get_role_by_name


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    result = await session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    result = await session.execute(select(User).where(User.user_name == username))
    return result.scalar_one_or_none()


async def get_users(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User))
    return list(result.scalars().all())


async def create_user(session: AsyncSession, user: User, role_name: str = "user") -> User:
    role_obj = await get_role_by_name(session, role_name)

    if role_obj is None:
        role_obj = Role(name=role_name, description=role_name)
        session.add(role_obj)
        await session.flush()

    user.role = role_obj
    session.add(user)

    await session.commit()
    await session.refresh(user)

    return user


async def update_user(session: AsyncSession, user: User, update_data: dict) -> User:
    result = await base.update(session, user, update_data)
    return result


async def delete_user(session: AsyncSession, user: User) -> None:
    await session.delete(user)
    await session.commit()
