from datetime import date

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.api.v1.note.router import note_router
from src.integrations.postgres import get_session
from src.integrations.redis.cache import redis_get, redis_set
from src.schema.models.note import NotePageResp, NoteResp
from src.utils.auth.jwt import JwtTokenT, jwt_auth
from src.utils.crud.note import get_note, get_notes_page, get_notes_total_rows


@note_router.get('/{note_id}', status_code=status.HTTP_200_OK, response_model=NoteResp)
async def get_user_note(
    note_id: int,
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
    session: AsyncSession = Depends(get_session),
) -> NoteResp:
    note = await get_note(session, access_token['user_id'], note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return note


@note_router.get('', status_code=status.HTTP_200_OK, response_model=NotePageResp)
async def get_user_notes(
    offset: int,
    limit: int,
    notes_date: date = date.today(),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
    session: AsyncSession = Depends(get_session),
) -> NotePageResp:
    redis_page = await redis_get(str(access_token['user_id']), str(notes_date) + str(offset))
    if redis_page:
        return redis_page
    notes = await get_notes_page(session, access_token['user_id'], offset, limit, notes_date)
    if not notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    page_data = {'notes': notes, 'total_rows': await get_notes_total_rows(session, access_token['user_id'], notes_date)}
    result = NotePageResp.model_validate(page_data)
    await redis_set(str(access_token['user_id']), str(notes_date) + str(offset), NotePageResp.model_dump(result))
    return result
