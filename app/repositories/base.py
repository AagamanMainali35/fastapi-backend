# Base repo for all global updtaes

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession


async def update(session: AsyncSession, instance: Any, update_data: dict) -> Any:
    for field, value in update_data.items():
        setattr(instance, field, value)

    await session.commit()
    await session.refresh(instance)

    return instance
