import asyncio

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import AsyncSessionLocal
from app.core.security import hash_password
from app.domains.auth.models import User  # Needed to register User in SQLAlchemy mapper
from app.domains.auth.repository import create_user
from app.domains.roles.models import Permission, Role

permissions = [
    {"name": "users:create", "description": "Create users"},
    {"name": "users:read", "description": "Read users"},
    {"name": "users:update", "description": "Update users"},
    {"name": "users:delete", "description": "Delete users"},
    {"name": "roles:create", "description": "Create roles"},
    {"name": "roles:read", "description": "Read roles"},
    {"name": "roles:update", "description": "Update roles"},
    {"name": "roles:delete", "description": "Delete roles"},
]


roles = [{"name": "admin", "description": "Administrator"}, {"name": "user", "description": "user"}]


async def seed():
    async with AsyncSessionLocal() as session:

        for permission in permissions:
            result = await session.execute(select(Permission).where(Permission.name == permission["name"]))

            existing = result.scalar_one_or_none()

            if not existing:
                session.add(Permission(**permission))

        await session.commit()

        for role in roles:
            result = await session.execute(select(Role).where(Role.name == role["name"]))

            existing = result.scalar_one_or_none()

            if not existing:
                session.add(Role(**role))

        await session.commit()

        admin = await session.execute(select(Role).options(selectinload(Role.permissions)).where(Role.name == "admin"))

        user = await session.execute(select(Role).options(selectinload(Role.permissions)).where(Role.name == "user"))

        user_role = user.scalar_one()

        admin_role = admin.scalar_one()

        admin_user_result = await session.execute(select(User).where(User.email == "admin@admin.com"))
        if not admin_user_result.scalar_one_or_none():
            new_admin = User(
                email="admin@admin.com",
                user_name="admin",
                hashed_password=hash_password("123"),
                is_verified=True,
            )
            await create_user(session, new_admin, role_name="admin")
            print("Admin user created successfully.")

        admin_perms = await session.execute(select(Permission))

        user_perms = await session.execute(
            select(Permission).where(
                Permission.name.in_(
                    [
                        "users:read",
                        "users:create",
                        "users:update",
                        "users:delete",
                    ]
                )
            )
        )

        user_role.permissions = user_perms.scalars().all()

        admin_role.permissions = admin_perms.scalars().all()

        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed())
