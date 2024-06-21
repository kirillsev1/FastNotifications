from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import Response

from src.api.v1.note.router import note_router
from src.integrations.postgres import get_session
from src.utils.auth.jwt import JwtTokenT, jwt_auth
from src.utils.crud.note import delete_note


@note_router.delete(
    '/{note_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(jwt_auth.validate_token)],
)
async def put_note(
    note_id: int,
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
    session: AsyncSession = Depends(get_session),
) -> Response:
    if not await delete_note(session, access_token['user_id'], note_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
