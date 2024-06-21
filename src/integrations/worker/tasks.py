from asyncio import new_event_loop, set_event_loop
from datetime import datetime, timedelta, timezone

import pytz
from aiogram import Bot

from src.conf.config import settings
from src.integrations.postgres import get_session
from src.integrations.worker.celery import app
from src.models.calendar.note import Note
from src.utils.crud.note import get_note

bot = Bot(settings.BOT_TOKEN)
loop = new_event_loop()
set_event_loop(loop)

plan = [
    {'hours': 12},
    {'minutes': 5},
    {'minutes': 1},
]


async def main(chat_id: int, user_id: int, note_id: int) -> None:
    async for session in get_session():
        note = await get_note(session, user_id, note_id)
        if note is not None:
            await bot.send_message(chat_id, note.content)


@app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={'max_retries': 5}
)
def send_notification_task(_, chat_id: int, user_id: int, note_id: int) -> bool:
    loop.run_until_complete(main(chat_id, user_id, note_id))
    return True


async def schedule_notifications(chat_id: int, note: Note) -> None:
    eta = note.perform.astimezone(pytz.UTC)
    for schedule_time in plan:
        delta = timedelta(**schedule_time)
        if datetime.now(timezone.utc) + delta < eta:
            task_id = f'note:plan:{note.id}:{int(delta.total_seconds())}'
            send_notification_task.apply_async(args=(chat_id, note.user_id, note.id), eta=eta - delta, task_id=task_id)


async def revoke_notifications(note_id: int) -> None:
    from src.integrations.worker.celery import app

    for schedule_time in plan:
        delta = timedelta(**schedule_time)
        task_id = f'note:plan:{note_id}:{int(delta.total_seconds())}'
        print(task_id)
        print(app.control.revoke(task_id, terminate=True))
