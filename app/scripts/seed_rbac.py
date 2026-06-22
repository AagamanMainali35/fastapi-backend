import asyncio

from sqlalchemy import select

from app.core.db import AsyncSessionLocal
from app.domains.auth.models import Permission, Role

permissions = [
    {"name": "users:create", "description": "Create users"},
    {"name": "users:read", "description": "Read users"},
    {"name": "users:update", "description": "Update users"},
    {"name": "users:delete", "description": "Delete users"},
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

        admin = await session.execute(select(Role).where(Role.name == "admin"))

        user = await session.execute(select(Role).where(Role.name == "user"))

        user_role = user.scalar_one()

        admin_role = admin.scalar_one()

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
