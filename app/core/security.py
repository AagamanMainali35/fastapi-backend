# Security utilities (e.g., password hashing, JWT generation)
"""Password hashing (Argon2 via pwdlib) and JWT helpers (PyJWT)."""

from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from app.core.config import settings

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Hash a plain text password."""
    return password_hash.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """Verify a plain text password against a hashed password."""
    return password_hash.verify(password, hashed)


def _create_token(subject: str | int, token_type: str, expires_delta: timedelta) -> str:
    """Create a JWT token with subject, type, and expiration claims."""
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(subject),
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_access_token(subject: str | int) -> str:
    """Create a short-lived access token for authentication."""
    return _create_token(
        subject,
        "access",
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )


def create_refresh_token(subject: str | int) -> str:
    """Create a long-lived refresh token for generating new access tokens."""
    return _create_token(
        subject,
        "refresh",
        timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )


def decode_token(token: str) -> dict:
    """Decode and validate a JWT token."""
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
