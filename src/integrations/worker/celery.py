from celery import Celery  # type: ignore

from src.conf.config import settings

app = Celery(
    'worker',
    broker=settings.CELERY_BROKER_URL,
    include=['src.integrations.worker.tasks'],
    debug=True,
    enable_utc='Europe/Moscow',
)

app.autodiscover_tasks()
