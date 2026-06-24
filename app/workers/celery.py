from celery import Celery

from app.core.config import settings

redis_url = f"redis://{settings.REDIS_HOST}:" f"{settings.REDIS_PORT}/" f"{settings.REDIS_DB}"


celery_app = Celery(
    "fastapi_app",
    broker=redis_url,
    backend=redis_url,
)

celery_app.autodiscover_tasks(["app.workers"], related_name="task")
