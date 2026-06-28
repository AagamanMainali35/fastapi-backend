"""Data-access layer for auth domain (repository pattern)."""

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.users.models import User
from app.repositories.role import get_role_by_name


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
