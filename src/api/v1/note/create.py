from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.api.v1.note.router import note_router
from src.integrations.postgres import get_session
from src.integrations.worker.tasks import schedule_notifications
from src.schema.models.note import NoteReq, NoteResp
from src.utils.auth.jwt import JwtTokenT, jwt_auth
from src.utils.crud.note import create_note
from src.utils.crud.user import get_user_utc


@note_router.post('', status_code=status.HTTP_201_CREATED, response_model=NoteResp)
async def create(
        body: NoteReq,
        access_token: JwtTokenT = Depends(jwt_auth.validate_token),
        session: AsyncSession = Depends(get_session),
) -> NoteResp:
    note_data = body.model_dump()
    note_data['user_id'] = access_token['user_id']

    note = await create_note(session, note_data)
    if note_data['send_required']:
        try:
            await schedule_notifications(access_token['chat_id'], note)
        except Exception as error:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    return note


