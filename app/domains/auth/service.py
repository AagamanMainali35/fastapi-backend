"""Auth domain business logic."""

import secrets
import string
from datetime import datetime, timedelta, timezone

import httpx
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import AppException
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.domains.auth.exceptions import (
    EmailVerificationError,
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserNotVerifiedError,
)
from app.domains.auth.models import User
from app.domains.auth.repository import (
    create_user,
    get_user_by_email,
    get_user_by_username,
    mark_user_verified,
    update_verification_code,
)
from app.workers.task import send_verification_email_task


class AuthService:
    """Handles registration, login, and OAuth flows."""

    @staticmethod
    async def register_user(session: AsyncSession, email: str, username: str, password: str) -> User:
        existing_email = await get_user_by_email(session, email)
        if existing_email:
            raise UserAlreadyExistsError(message="Email already exists")

        existing_username = await get_user_by_username(session, username)
        if existing_username:
            raise UserAlreadyExistsError(message="Username already exists")

        user = User(email=email, user_name=username, hashed_password=hash_password(password))

        user = await create_user(session, user)

        code = "".join(secrets.choice(string.digits) for _ in range(6))
        hashed_code = hash_password(code)
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.VERIFICATION_CODE_EXPIRE_MINUTES)

        await update_verification_code(session, user, hashed_code, expires_at)

        try:
            send_verification_email_task.delay(user.email, code)
        except Exception:
            pass

        return user

    @staticmethod
    async def login(session: AsyncSession, email: str, password: str) -> dict:
        user = await get_user_by_email(session, email)

        if not user:
            raise InvalidCredentialsError(code=401, message="Invalid credentials")

        if not user.is_verified:
            raise UserNotVerifiedError()

        if not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError(code=401, message="Invalid credentials")

        return {
            "access_token": create_access_token(subject=user.id),
            "refresh_token": create_refresh_token(user.id),
            "token_type": "bearer",
        }

    @staticmethod
    async def verify_email(session: AsyncSession, email: str, code: str) -> dict:
        user = await get_user_by_email(session, email)
        if not user:
            raise EmailVerificationError()

        if user.is_verified:
            return {"message": "Email is already verified"}

        if not user.verification_code or not user.verification_code_expires_at:
            raise EmailVerificationError()

        if datetime.now(timezone.utc) > user.verification_code_expires_at:
            raise EmailVerificationError(message="Verification code has expired")

        if not verify_password(code, user.verification_code):
            raise EmailVerificationError(message="Invalid verification code")

        await mark_user_verified(session, user)
        return {"message": "Email successfully verified"}

    @staticmethod
    async def resend_verification_code(session: AsyncSession, email: str) -> dict:
        user = await get_user_by_email(session, email)
        if not user:
            return {"message": "If the email is registered, a new verification code has been sent"}

        if user.is_verified:
            return {"message": "Email is already verified"}

        code = "".join(secrets.choice(string.digits) for _ in range(6))
        hashed_code = hash_password(code)
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.VERIFICATION_CODE_EXPIRE_MINUTES)

        await update_verification_code(session, user, hashed_code, expires_at)

        try:
            send_verification_email_task.delay(user.email, code)
        except Exception:
            pass  # Non-blocking on email failure for now

        return {"message": "A new verification code has been sent"}

    @staticmethod
    async def google_login_or_register(session: AsyncSession, email: str, name: str, google_id: str) -> dict:
        user = await get_user_by_email(session, email)

        if not user:
            # Generate random password for social login user
            alphabet = string.ascii_letters + string.digits + string.punctuation
            random_password = "".join(secrets.choice(alphabet) for _ in range(32))

            # Create a unique username from email prefix
            username_base = email.split("@")[0]
            random_suffix = "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6))
            username = f"{username_base}_{random_suffix}"

            new_user = User(
                email=email,
                user_name=username,
                hashed_password=hash_password(random_password),
                google_id=google_id,
            )
            user = await create_user(session, new_user)

        return {
            "access_token": create_access_token(subject=user.id),
            "refresh_token": create_refresh_token(user.id),
            "token_type": "bearer",
        }

    @staticmethod
    async def exchange_google_code(code: str, redirect_uri: str) -> dict:
        """Exchange Google authorization code for user info.

        Returns a dict with keys: email, google_id, name.
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": redirect_uri,
                },
            )

        if response.status_code != 200:
            raise AppException(
                message="Failed to exchange authorization code with Google",
                code=400,
                errors={"detail": response.text},
            )

        token_data = response.json()

        if "id_token" not in token_data:
            raise AppException(message="No ID token found in Google response", code=400, errors=token_data)

        google_token = token_data["id_token"]

        try:
            google_user = id_token.verify_oauth2_token(
                google_token,
                google_requests.Request(),
                settings.GOOGLE_CLIENT_ID,
                clock_skew_in_seconds=10,
            )
        except ValueError as e:
            raise AppException(message=f"Invalid Google ID token: {str(e)}", code=400)

        return {
            "email": google_user["email"],
            "google_id": google_user["sub"],
            "name": google_user.get("name"),
        }
