from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.auth.models import Role, User


async def get_user_by_email(session: AsyncSession, email: str):
    result = await session.execute(select(User).where(User.email == email))

    return result.scalar_one_or_none()


async def get_user_by_username(session: AsyncSession, username: str):
    result = await session.execute(select(User).where(User.user_name == username))

    return result.scalar_one_or_none()


async def get_role_by_name(session: AsyncSession, role_name):
    result = await session.execute(select(Role).where(Role.name == role_name))

    role_obj = result.scalar_one_or_none()
    return role_obj


async def create_role(session: AsyncSession, role):
    role_obj = await session.add(role)
    return role_obj


async def create_user(session: AsyncSession, user: User):
    role_obj = await get_role_by_name(session, "user")

    if role_obj is None:
        role_obj = Role(name="user", description="user")
        session.add(role_obj)
        await session.flush()

    user.role = role_obj
    session.add(user)

    await session.commit()

    await session.refresh(user)

    return user
