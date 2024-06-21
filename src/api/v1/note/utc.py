from json import dumps
from typing import Dict

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.orm.base import _T_co
from starlette import status
from starlette.responses import Response

from src.api.v1.note.router import note_router
from src.integrations.postgres import get_session
from src.utils.auth.jwt import JwtTokenT, jwt_auth
from src.utils.crud.user import patch_user_utc, get_user_utc


@note_router.patch(
    '/utc',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(jwt_auth.validate_token)],
)
async def patch_utc(
        utc: int,
        access_token: JwtTokenT = Depends(jwt_auth.validate_token),
        session: AsyncSession = Depends(get_session),
) -> None:
    await patch_user_utc(session, access_token['user_id'], utc)


@note_router.get(
    '/utc',
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(jwt_auth.validate_token)],
    response_description=dict[str, int]
)
async def get_utc(
        access_token: JwtTokenT = Depends(jwt_auth.validate_token),
        session: AsyncSession = Depends(get_session),
) -> dict[str, int]:
    utc = {'utc': await get_user_utc(session, access_token['user_id'])}
    return utc
