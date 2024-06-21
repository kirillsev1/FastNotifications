from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Annotated, Any, cast

from fastapi import Header, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import TypedDict

from src.conf.config import settings
from src.models.calendar.user import User
from src.utils.auth.password import hash_password

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


class JwtTokenT(TypedDict):
    uid: str
    user_id: int
    chat_id: int
    exp: datetime


@dataclass
class JwtAuth:
    secret: str

    def create_token(self, user_id: int, chat_id: int) -> str:
        access_token = {
            'user_id': user_id,
            'chat_id': chat_id,
            'exp': datetime.utcnow() + timedelta(days=6),
        }
        return jwt.encode(access_token, self.secret)

    def validate_token(self, access_token: Annotated[str, Header()]) -> JwtTokenT:
        try:
            return cast(JwtTokenT, jwt.decode(access_token, self.secret))
        except JWTError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


jwt_auth = JwtAuth(settings.JWT_SECRET_SALT)


async def get_user(session: AsyncSession, user_info: Any) -> User | None:
    return (
        await session.scalars(
            select(User).where(
                User.tg_id == user_info.tg_id,
                User.password == hash_password(user_info.password),
            )
        )
    ).one_or_none()


async def authenticate_user(session: AsyncSession, user_data: Any) -> User:
    user = await get_user(session, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect login or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return user


def create_access_token(data: dict[str, Any], expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def data_from_access_token(token: str) -> dict[str, Any]:
    decoded_jwt = jwt.decode(token, SECRET_KEY)
    return decoded_jwt
