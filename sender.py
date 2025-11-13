import smtplib
from email.message import EmailMessage
from typing import List, Optional
from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env
load_dotenv()

def send_email(
    smtp_host: str,
    smtp_port: int,
    username: str,
    password: str,
    subject: str,
    body: str,
    to: List[str],
    cc: Optional[List[str]] = None,
    use_ssl: bool = False,
    from_name: Optional[str] = None,
) -> bool:
    try:
        msg = EmailMessage()
        sender_email = username
        msg["From"] = f"{from_name} <{sender_email}>" if from_name else sender_email
        msg["To"] = ", ".join(to)
        if cc:
            msg["Cc"] = ", ".join(cc)
        msg["Subject"] = subject
        msg.set_content(body)

        recipients = to + (cc or [])

        if use_ssl:
            server = smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=20)
        else:
            server = smtplib.SMTP(smtp_host, smtp_port, timeout=20)
            server.ehlo()
            server.starttls()
            server.ehlo()

        server.login(username, password)
        server.send_message(msg, from_addr=sender_email, to_addrs=recipients)
        server.quit()
        return True

    except Exception as e:
        print("Erro ao enviar e-mail:", e)
        return False


def exemplo_uso_envio(corpo: str):
    # Carrega as variáveis do .env
    SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    USERNAME = os.getenv("SMTP_USER", "")
    PASSWORD = os.getenv("SMTP_PASS", "")
    FROM_NAME = os.getenv("FROM_NAME", "teste_envio_de_emails")

    # Listas de destinatários e cópia (se existir)
    destinatarios = os.getenv("MAIL_TO", "").split(",")
    cc_raw = os.getenv("MAIL_CC", "")
    cc = [c.strip() for c in cc_raw.split(",") if c.strip()] if cc_raw else None

    assunto = "Confirmação de recebimento dos dados"

    enviado = send_email(
        smtp_host=SMTP_HOST,
        smtp_port=SMTP_PORT,
        username=USERNAME,
        password=PASSWORD,
        subject=assunto,
        body=corpo,
        to=destinatarios,
        cc=cc,
        use_ssl=bool(int(os.getenv("USE_SSL", 0))),  # 1 ou 0 no .env
        from_name=FROM_NAME,
    )

    if enviado:
        print("✅ E-mail enviado com sucesso!")
    else:
        print("❌ Falha ao enviar o e-mail.")