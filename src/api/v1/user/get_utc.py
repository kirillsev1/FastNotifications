from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from src.api.v1.user.router import user_router
from src.integrations.postgres import get_session
from src.utils.auth.jwt import JwtTokenT, jwt_auth
from src.utils.crud.user import get_user_utc


@user_router.get(
    '/utc',
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(jwt_auth.validate_token)],
)
async def get_utc(
        access_token: JwtTokenT = Depends(jwt_auth.validate_token),
        session: AsyncSession = Depends(get_session),
) -> JSONResponse:
    utc = {'utc': await get_user_utc(session, access_token['user_id'])}
    return JSONResponse(content=utc)

