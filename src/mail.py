from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

conf = ConnectionConfig(
    MAIL_FROM="abracadabra@eshkere.com",
    MAIL_PASSWORD="6f86fa14cb051c",
    MAIL_FROM_NAME="Freelance Exchange",
    MAIL_USERNAME="a701dadb85d23c",
    MAIL_PORT=2525,
    MAIL_SERVER="sandbox.smtp.mailtrap.io",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=False,
    VALIDATE_CERTS=False,
)

fastmail = FastMail(conf)