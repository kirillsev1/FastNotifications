from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.api.v1.auth.router import auth_router
from src.integrations.postgres import get_session
from src.schema.auth.token import Info, Login, Token
from src.utils.auth.jwt import JwtTokenT, authenticate_user, jwt_auth


@auth_router.post('/info', response_model=Info, status_code=status.HTTP_200_OK)
async def info(access_token: JwtTokenT = Depends(jwt_auth.validate_token)) -> Info:
    return Info.model_validate(access_token)


@auth_router.post('/login', response_model=Token)
async def login_for_access_token(
    form_data: Login,
    session: AsyncSession = Depends(get_session),
) -> Token:
    user = await authenticate_user(session, form_data)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = jwt_auth.create_token(user.id, user.tg_id)
    return Token(access_token=access_token, token_type='bearer')
