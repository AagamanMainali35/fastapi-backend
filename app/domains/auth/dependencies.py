"""Shared API dependencies (authentication, authorization)."""

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.exceptions import AppException
from app.core.security import decode_token
from app.domains.users.models import User
from app.repositories.user import get_user_by_id

security_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),  # noqa: B008
    session: AsyncSession = Depends(get_db),  # noqa: B008
) -> User:
    """Decode JWT and return the authenticated user."""
    try:
        payload = decode_token(credentials.credentials)
        user_id = int(payload["sub"])
    except Exception:
        raise AppException(message="Invalid or expired token", code=401)

    user = await get_user_by_id(session, user_id)
    if not user:
        raise AppException(message="User not found", code=401)

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),  # noqa: B008
) -> User:
    """Ensure the authenticated user is active."""
    if not current_user.is_active:
        raise AppException(message="Inactive user account", code=403)
    return current_user
