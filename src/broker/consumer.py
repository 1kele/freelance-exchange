import asyncio
import json

from pika import BlockingConnection, ConnectionParameters
from src.celery_tasks.tasks import _create_pdf_report_async
from src.config import settings

connection_parameters = ConnectionParameters(
    host=settings.RABBITMQ_HOST,
    port=settings.RABBITMQ_PORT,
)

def callback(ch, method, propertie, body):
    try:
        print(body)
        data = json.loads(body)
        if data["type"] == "create_pdf_report":
            asyncio.run(
                _create_pdf_report_async(
                    user_id=data["user_id"],
                    date_from=data["date_from"],
                    date_to=data["date_to"],
                )
            )
        else:
            print("UNKNOWN MESSAGE TYPE")

        ch.basic_ack(delivery_tag=method.delivery_tag)

        print("PDF REPORT CREATED")
    except Exception as e:
        print("ERROR:", e)

        ch.basic_ack(
            delivery_tag=method.delivery_tag
        )


def main():
    with BlockingConnection(connection_parameters) as conn:
        ch = conn.channel()
        ch.queue_declare(queue="tasks")

        ch.basic_consume(
            queue="tasks",
            on_message_callback=callback,
        )
        print("WAITING FOR MESSAGES")
        ch.start_consuming()


if __name__ == "__main__":
    main()