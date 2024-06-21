import hashlib
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.calendar.user import User


def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()


async def create_user(session: AsyncSession, user_dict: dict[str, Any]) -> User:
    user_dict['password'] = hash_password(user_dict['password'])
    user = User(**user_dict)
    async with session.begin_nested():
        session.add(user)
        await session.flush()
        await session.commit()
    return user


async def patch_user_utc(session: AsyncSession, user_id: int, utc: int):
    user = await session.get(User, user_id)
    user.utc = utc
    await session.commit()


async def get_user_utc(session: AsyncSession, user_id: int):
    user = await session.get(User, user_id)
    return user.utc
