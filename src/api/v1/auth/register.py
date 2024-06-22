from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.api.v1.auth.router import auth_router
from src.integrations.postgres import get_session
from src.schema.auth.user import UserReq, UserResp
from src.utils.crud.user import create_user


@auth_router.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserResp)
async def create(
    body: UserReq,
    session: AsyncSession = Depends(get_session),
) -> UserResp:
    user_data = body.model_dump()
    try:
        user = await create_user(session, user_data)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return user
