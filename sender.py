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

def exemplo_uso_envio(corpo):
    #Algumas configurações podem variar de acordo com seu provedor de e-mail
    SMTP_HOST = "smtp.gmail.com"
    SMTP_PORT = 587                          # 587=STARTTLS, 465=SSL
    USERNAME = ""                            #Seu endereço de e-mail
    PASSWORD = ""                            #Senha ou APP Password do seu e-mail. para Gmail, gere sua APP Password em: https://myaccount.google.com/apppasswords 
    FROM_NAME = "teste_envio_de_emails"      #Alias que substituí o nome do endereço de e-mail

    destinatarios = [""] #Destinatário/s do e-mail
    #cc = ["copia@exemplo.com"]  # cópias do e-mail ou None para nenhum, descomente para enviar e-mail com cópias junto à linha 72

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
