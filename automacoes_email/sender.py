import smtplib
from email.message import EmailMessage
from typing import List, Optional


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
    """
    Envia um e-mail simples (texto) usando SMTP.
    Retorna True se enviado com sucesso, False caso contrário.

    - smtp_host: host do servidor SMTP (ex: "smtp.gmail.com")
    - smtp_port: porta (ex: 587 para STARTTLS, 465 para SSL)
    - username/password: credenciais do mailbox (ou app password para Gmail)
    - to: lista de destinatários
    - cc: lista de cópias (opcional)
    - use_ssl: se True usa smtplib.SMTP_SSL (porta 465), se False usa STARTTLS (porta 587)
    - from_name: nome exibido como remetente (opcional)
    """
    try:
        msg = EmailMessage()
        sender_email = username
        if from_name:
            msg['From'] = f"{from_name} <{sender_email}>"
        else:
            msg['From'] = sender_email

        msg['To'] = ", ".join(to)
        if cc:
            msg['Cc'] = ", ".join(cc)
        msg['Subject'] = subject

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


# ---------------------------
# Exemplo de integração com a função faker()
# ---------------------------

def exemplo_uso_envio(corpo):
    # Ajuste estas variáveis com seus dados/servidor
    SMTP_HOST = "smtp.gmail.com"
    SMTP_PORT = 587               # 587=STARTTLS, 465=SSL
    USERNAME = "lucaslyra729@gmail.com"
    PASSWORD = "dgtajebvofghykko"  # nunca versionar isto em repos públicos!
    FROM_NAME = "Equipe Atendimento"

    destinatarios = ["lucaslyra729@gmail.com"]
    #cc = ["copia@exemplo.com"]  # ou None

    assunto = "Confirmação de recebimento dos dados"

    enviado = send_email(
        smtp_host=SMTP_HOST,
        smtp_port=SMTP_PORT,
        username=USERNAME,
        password=PASSWORD,
        subject=assunto,
        body=corpo,
        to=destinatarios,
     #   cc=cc,
        use_ssl=False,    # True se usar porta 465
        from_name=FROM_NAME
    )

    if enviado:
        print("E-mail enviado com sucesso!")
    else:
        print("Falha ao enviar o e-mail.")


# Se quiser testar diretamente:
# exemplo_uso_envio()