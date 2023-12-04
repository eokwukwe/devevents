from pathlib import Path
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

from app.utils.config import settings


conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM="devevents@email.com",
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_FROM_NAME="Team Devevents",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent.parent / 'templates',
)

email_client = FastMail(conf)
MessageSchema = MessageSchema
MessageType = MessageType

