from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr

from app.core.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.SMTP_USER,
    MAIL_PASSWORD=settings.SMTP_PASSWORD,
    MAIL_FROM=settings.SMTP_FROM_EMAIL,
    MAIL_PORT=settings.SMTP_PORT,
    MAIL_SERVER=settings.SMTP_HOST,
    MAIL_FROM_NAME=settings.SMTP_FROM_NAME,
    MAIL_STARTTLS=settings.SMTP_USE_TLS,
    MAIL_SSL_TLS=settings.SMTP_USE_SSL,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

fast_mail = FastMail(conf)


async def send_verification_email(email: str, code: str) -> None:
    html = f"""
    <p>Your verification code is: <strong>{code}</strong></p>
    <p>This code will expire in {settings.VERIFICATION_CODE_EXPIRE_MINUTES} minutes.</p>
    """

    message = MessageSchema(
        subject="Email Verification Code",
        recipients=[email],
        body=html,
        subtype=MessageType.html,
    )

    await fast_mail.send_message(message)
