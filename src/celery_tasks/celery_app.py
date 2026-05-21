from celery import Celery

celery_instance = Celery(
    "celery_tasks",
    broker="amqp://guest:guest@localhost:5672//",
    include=["src.celery_tasks.tasks"],
)
