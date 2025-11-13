import requests
import sender
import time
from datetime import datetime

API_URL = "https://api.invertexto.com/v1/faker?token=22881|Bqwh6BfkXZzKQ06LhoTO0TrnDHD0SYEN&fields=name,cpf&locale=pt_BR"
CPFS_FILE = "cpfs_enviados.txt"

def obter_dados_faker():
    """Retorna (nome, cpf) ou (None, None) em caso de erro."""
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print("Erro ao chamar API:", e)
        return None, None

    data = response.json()
    nome = data.get("name")
    cpf = data.get("cpf")

    if not nome or not cpf:
        print("Resposta da API não contém nome/cpf:", data)
        return None, None

    return nome, cpf

def gerar_corpo_email(nome: str, cpf: str) -> str:
    corpo = f"""
    Prezado(a) {nome},

    Esperamos que esteja bem!

    Estamos entrando em contato para confirmar o recebimento dos seus dados fictícios:
    - Nome: {nome}
    - CPF: {cpf}

    Atenciosamente,
    Equipe de Atendimento
    """
    return corpo.strip()
#função de clock antiga
def registrar_cpf_enviado(cpf: str, arquivo: str = CPFS_FILE):
    """Anexa o CPF ao arquivo com timestamp UTC (uma linha por envio)."""
    ts = datetime.utcnow().isoformat()
    with open(arquivo, "a", encoding="utf-8") as f:
        f.write(f"{ts} {cpf}\n")

def enviar_n_emails(n: int, delay_s: float = 0.5):
    for i in range(n):
        nome, cpf = obter_dados_faker()
        if not nome or not cpf:
            print(f"[{i+1}/{n}] Pulando envio: dados inválidos.")
            time.sleep(delay_s)
            continue

        corpo = gerar_corpo_email(nome, cpf)

        try:
            sender.exemplo_uso_envio(corpo)  
            registrar_cpf_enviado(cpf)
            print(f"[{i+1}/{n}] Enviado para {nome} ({cpf}) — registrado.")
        except Exception as e:
            print(f"[{i+1}/{n}] Falha ao enviar o e-mail para {nome} ({cpf}):", e)

        time.sleep(delay_s)

if __name__ == "__main__":
    enviar_n_emails(50)
