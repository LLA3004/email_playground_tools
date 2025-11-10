import requests
import sender

url = "https://api.invertexto.com/v1/faker?token=22881|Bqwh6BfkXZzKQ06LhoTO0TrnDHD0SYEN&fields=name,cpf&locale=pt_BR"
response = requests.get(url)

def faker():
    if response.status_code == 200:
        data = response.json()
        print("Resposta da API:", data)

        # Usa o próprio dicionário retornado
        corpo = gerar_corpo_email(data["name"], data["cpf"])
        print("\n=== Corpo do E-mail ===\n")
        print(corpo)
        return corpo
    else:
        print('A requisição falhou com o código de status:', response.status_code)

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

# Executa a função
sender.exemplo_uso_envio(faker())
