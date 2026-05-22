from celery import Celery

from src.config import settings

celery_instance = Celery(
    "celery_tasks",
    broker=settings.RABBITMQ_URL,
    include=["src.celery_tasks.tasks"],
)

