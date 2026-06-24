"""Data-access layer for auth domain (repository pattern)."""

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.auth.models import Role, User


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    result = await session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    result = await session.execute(select(User).where(User.user_name == username))
    return result.scalar_one_or_none()


async def get_role_by_name(session: AsyncSession, role_name: str) -> Role | None:
    result = await session.execute(select(Role).where(Role.name == role_name))
    return result.scalar_one_or_none()


async def create_role(session: AsyncSession, role: Role) -> Role:
    session.add(role)
    await session.flush()
    return role


async def create_user(session: AsyncSession, user: User) -> User:
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


async def update_verification_code(session: AsyncSession, user: User, hashed_code: str, expires_at: datetime) -> None:
    user.verification_code = hashed_code
    user.verification_code_expires_at = expires_at
    await session.commit()
    await session.refresh(user)


async def mark_user_verified(session: AsyncSession, user: User) -> None:
    user.is_verified = True
    user.verification_code = None
    user.verification_code_expires_at = None
    await session.commit()
    await session.refresh(user)
