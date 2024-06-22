from datetime import date
from typing import Any, Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.metrics import async_integrations_timer
from src.models.calendar.note import Note
from src.schema.models.note import NoteReq


@async_integrations_timer
async def create_note(session: AsyncSession, note_data: dict[str, Any]) -> Note:
    async with session.begin_nested():
        instance = Note(**note_data)
        session.add(instance)
        await session.flush()
        await session.commit()
    return instance


@async_integrations_timer
async def update_note(session: AsyncSession, model: Note, updated: NoteReq) -> None:
    note_dict = updated.model_dump()
    for attr, value in note_dict.items():
        setattr(model, attr, value)

    await session.commit()


@async_integrations_timer
async def patch_note(session: AsyncSession, model: Note, field: str, value: Any) -> None:
    setattr(model, field, value)
    await session.commit()


@async_integrations_timer
async def get_note(session: AsyncSession, user_id: int, note_id: int) -> Note | None:
    return (await session.scalars(select(Note).where(Note.user_id == user_id, Note.id == note_id))).first()


@async_integrations_timer
async def get_notes_page(
    session: AsyncSession, user_id: int, offset: int, limit: int, notes_date: date
) -> Sequence[Note]:
    return (
        await session.scalars(
            select(Note)
            .where(Note.user_id == user_id, func.Date(Note.perform) == notes_date)
            .limit(limit)
            .offset(offset)
            .order_by(Note.perform, Note.created, Note.id)
        )
    ).all()


@async_integrations_timer
async def get_notes_total_rows(session: AsyncSession, user_id: int, notes_date: date) -> Sequence[Note]:
    return await session.scalar(
        select(func.count()).select_from(Note).where(Note.user_id == user_id, func.Date(Note.perform) == notes_date)
    )


async def delete_note(session: AsyncSession, user_id: int, note_id: int) -> bool:
    note = await session.get(Note, note_id)
    if not note or note.user_id != user_id:
        return False
    await session.delete(note)
    await session.commit()
    return True
