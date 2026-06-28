from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UserAlreadyExistsError, UserNotFoundError
from app.core.security import hash_password
from app.domains.users.models import User
from app.repositories import user as repository


class UserService:
    @staticmethod
    async def get_user(session: AsyncSession, user_id: int) -> User:
        user = await repository.get_user_by_id(session, user_id)
        if not user:
            raise UserNotFoundError()
        return user

    @staticmethod
    async def get_all_users(session: AsyncSession) -> list[User]:
        return await repository.get_users(session)

    @staticmethod
    async def create_user(session: AsyncSession, user_data: dict) -> User:
        email = user_data.get("email")
        if email:
            existing_email = await repository.get_user_by_email(session, email)
            if existing_email:
                raise UserAlreadyExistsError(message="Email already exists")

        username = user_data.get("username")
        if username:
            existing_username = await repository.get_user_by_username(session, username)
            if existing_username:
                raise UserAlreadyExistsError(message="Username already exists")

        hashed_password = ""
        password = user_data.get("password")
        if password:
            hashed_password = hash_password(password)

        new_user = User(
            email=email,
            user_name=username,
            hashed_password=hashed_password,
            is_active=user_data.get("is_active", True),
            is_verified=user_data.get("is_verified", False),
        )

        user = await repository.create_user(session, new_user)
        return user

    @staticmethod
    async def update_user(session: AsyncSession, user_id: int, update_data: dict) -> User:
        user = await UserService.get_user(session, user_id)

        email = update_data.get("email")
        if email and email != user.email:
            existing_email = await repository.get_user_by_email(session, email)
            if existing_email:
                raise UserAlreadyExistsError(message="Email already exists")

        username = update_data.get("username")
        if username and username != user.user_name:
            existing_username = await repository.get_user_by_username(session, username)
            if existing_username:
                raise UserAlreadyExistsError(message="Username already exists")

        db_update_data = {}
        if email:
            db_update_data["email"] = email
        if username:
            db_update_data["user_name"] = username
        if "password" in update_data and update_data["password"]:
            db_update_data["hashed_password"] = hash_password(update_data["password"])
        if "is_active" in update_data and update_data["is_active"] is not None:
            db_update_data["is_active"] = update_data["is_active"]
        if "is_verified" in update_data and update_data["is_verified"] is not None:
            db_update_data["is_verified"] = update_data["is_verified"]

        updated_user = await repository.update_user(session, user, db_update_data)
        return updated_user

    @staticmethod
    async def delete_user(session: AsyncSession, user_id: int) -> None:
        user = await UserService.get_user(session, user_id)
        await repository.delete_user(session, user)
