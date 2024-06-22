from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.api.v1.user.router import user_router
from src.integrations.postgres import get_session
from src.integrations.redis.cache import redis_set
from src.utils.auth.jwt import JwtTokenT, jwt_auth
from src.utils.crud.user import get_user_utc, patch_user_utc


@user_router.patch(
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

    await redis_set('utc', access_token['user_id'], {'utc': await get_user_utc(session, access_token['user_id'])})
