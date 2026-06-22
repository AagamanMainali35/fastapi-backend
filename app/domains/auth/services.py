from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.domains.auth.exceptions import InvalidCredentialsError, UserAlreadyExistsError
from app.domains.auth.models import User
from app.domains.auth.query import create_user, get_user_by_email, get_user_by_username


class Authservice:
    @staticmethod
    async def register_user(session: AsyncSession, email: str, username: str, password: str) -> User:

        existing_email = await get_user_by_email(session, email)
        if existing_email:
            raise UserAlreadyExistsError(message="Email already exists")

        existing_username = await get_user_by_username(session, username)
        if existing_username:
            raise UserAlreadyExistsError(message="Username already exists")

        user = User(email=email, user_name=username, hashed_password=hash_password(password))

        return await create_user(session, user)

    @staticmethod
    async def login(session, email, password):

        user = await get_user_by_email(session, email)

        if not user:
            raise InvalidCredentialsError(code=401, message="Invalid credentials")

        if not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError(code=401, message="Invalid credentials")

        return {"access_token": create_access_token(subject=user.id), "refresh_token": create_refresh_token(user.id), "token_type": "bearer"}

    @staticmethod
    async def google_login_or_register(session: AsyncSession, email: str, name: str, google_id: str):
        import secrets
        import string

        user = await get_user_by_email(session, email)

        if not user:
            # Generate random password for social login user
            alphabet = string.ascii_letters + string.digits + string.punctuation
            random_password = "".join(secrets.choice(alphabet) for i in range(32))

            # Create a unique username from email prefix
            username_base = email.split("@")[0]
            random_suffix = "".join(secrets.choice(string.ascii_lowercase + string.digits) for i in range(6))
            username = f"{username_base}_{random_suffix}"

            new_user = User(email=email, user_name=username, hashed_password=hash_password(random_password))
            user = await create_user(session, new_user)

        return {"access_token": create_access_token(subject=user.id), "refresh_token": create_refresh_token(user.id), "token_type": "bearer"}
