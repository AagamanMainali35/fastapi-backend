import asyncio

from app.core.email import send_verification_email
from app.workers.celery import celery_app


@celery_app.task
def send_verification_email_task(email: str, code: str):

    asyncio.run(send_verification_email(email, code))
