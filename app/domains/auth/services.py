from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.auth.models import User
from app.domains.auth.query import create_user, get_user_by_email


def perform_login(email: str, password: str):
    pass


def hash_password(password: str):
    return password


async def register_user(session: AsyncSession, email: str, username: str, password: str):

    existing = await get_user_by_email(session, email)

    if existing:
        raise Exception("Email already exists")

    user = User(email=email, user_name=username, hashed_password=hash_password(password))

    return await create_user(session, user)
