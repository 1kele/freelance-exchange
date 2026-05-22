import json

from pika import ConnectionParameters, BlockingConnection

from src.config import settings

connection_parameters = ConnectionParameters(
    host=settings.RABBITMQ_HOST,
    port=settings.RABBITMQ_PORT,
)

def publish_pdf_report(
    user_id: int,
    date_from: str,
    date_to: str,
):
    payload = {
        "type": "create_pdf_report",
        "user_id": user_id,
        "date_from": date_from,
        "date_to": date_to,
    }
    with BlockingConnection(connection_parameters) as conn:
        ch = conn.channel()
        ch.queue_declare(queue="tasks")
        ch.basic_publish(
            exchange="",
            routing_key="tasks",
            body=json.dumps(payload),
        )

        print("MESSAGE SENT")