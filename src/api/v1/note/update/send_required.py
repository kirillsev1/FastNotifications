from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import Response

from src.api.v1.note.router import note_router
from src.integrations.postgres import get_session
from src.integrations.worker.tasks import revoke_notifications, schedule_notifications
from src.utils.auth.jwt import JwtTokenT, jwt_auth
from src.utils.crud.note import get_note, patch_note


@note_router.patch(
    '/send_required/{note_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(jwt_auth.validate_token)],
)
async def path_note_send_required(
    send_required: bool,
    note_id: int,
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
    session: AsyncSession = Depends(get_session),
) -> Response:
    note = await get_note(session, access_token['user_id'], note_id)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if not send_required:
        await revoke_notifications(note_id)
    else:
        await schedule_notifications(note_id, note)

    await patch_note(session, note, 'send_required', send_required)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
