from celery import Celery

from api.core.config import settings

worker = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
    backend=f"db+{settings.database_url}",
)

worker.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
)

import api.core.dependencies.celery.tasks

if __name__ == "__main__":
    worker.start()
