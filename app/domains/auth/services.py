from pwdlib import PasswordHash
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.auth.models import User
from app.domains.auth.query import create_user, get_user_by_email

password_hash = PasswordHash.recommended()


class Authservice:

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using Argon2id and return the hashed value."""
        return password_hash.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against its hashed value."""
        return password_hash.verify(plain_password, hashed_password)

    @staticmethod
    async def register_user(session: AsyncSession, email: str, username: str, password: str) -> User:
        """
        Register a new user in the system.

        This asynchronous function handles user registration by validating that the provided
        email is not already registered, hashing the user's password, and creating a new
        user record in the database.

        Args:
            session (AsyncSession): The SQLAlchemy asynchronous database session used for
                database operations. The session must be active and properly managed by
                the caller (e.g., within an async context manager).
            email (str): The user's email address. Must be a valid email format and unique
                in the system. Case-sensitive comparison is performed during validation.
            username (str): The desired username for the new account. Must be unique and
                meet the application's username requirements (e.g., length, character set).
            password (str): The user's plain-text password. Will be hashed using the
                configured password hashing algorithm before storage. Must meet password
                strength requirements (e.g., minimum length, complexity).

        Returns:
            User: The newly created User ORM object, including the auto-generated user ID
                and any other default values set by the database (e.g., created_at timestamp).
        """
        existing = await get_user_by_email(session, email)

        if existing:
            raise Exception("Email already exists")

        user = User(email=email, user_name=username, hashed_password=Authservice.hash_password(password))

        return await create_user(session, user)
