import hashlib
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.metrics import async_integrations_timer
from src.models.calendar.user import User


def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()


@async_integrations_timer
async def create_user(session: AsyncSession, user_dict: dict[str, Any]) -> User:
    user_dict['password'] = hash_password(user_dict['password'])
    user = User(**user_dict)
    async with session.begin_nested():
        session.add(user)
        await session.flush()
        await session.commit()
    return user


@async_integrations_timer
async def patch_user_utc(session: AsyncSession, user_id: int, utc: int) -> None:
    user = await session.get(User, user_id)
    if user is not None:
        user.utc = utc
    await session.commit()


@async_integrations_timer
async def get_user_utc(session: AsyncSession, user_id: int) -> int | None:
    user = await session.get(User, user_id)
    if user is not None:
        return user.utc
    return None
