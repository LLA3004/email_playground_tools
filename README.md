Email Playground Tools — README
Visão geral

Email Playground Tools é uma pequena tool em Python para fins de aprendizado e testes:

shooter.py — consome a API Invertexto para gerar nome e CPF fictícios;

sender.py — envia e-mail via SMTP usando credenciais locais.

Estrutura do repositório
email_playground_tools/
├─ shooter.py         # gera nome e cpf (usa TOKEN)
├─ sender.py          # envia e-mail (lê .env via python-dotenv)
├─ .env.example       # modelo (sem dados sensíveis) — comitar
├─ .gitignore         # deve incluir .env — comitar
├─ README.md          # este arquivo
├─ README.md          # este arquivo


Instalação (rápido)

Clone o repositório:

git clone https://seu-repo.git
cd email_playground_tools


(Opcional) crie e ative um virtualenv:

python -m venv .venv
source .venv/bin/activate    # macOS / Linux
.venv\Scripts\Activate.ps1   # Windows PowerShell


# Instale dependências:
pip install requests python-dotenv

# Arquivo .env — o que é e por que NÃO comitar

O arquivo .env é local e normalmente contém credenciais sensíveis (token da API, usuário e senha do SMTP). NÃO comite esse arquivo para o GitHub. Para evitar vazamentos:

Adicione .env ao seu .gitignore

Exemplo seguro de .env.example:

# .env.example (APENAS MODELO)
#API Invertexto
INVERTEXTO_TOKEN=SEU_TOKEN_AQUI

#SMTP
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
USE_SSL=0               # 1 para SSL (porta 465), 0 para STARTTLS (porta 587)
SMTP_USER=seu_email@exemplo.com
SMTP_PASS=sua_app_password

#Remetente / destinatários
FROM_NAME=Nome do Remetente
MAIL_TO=destino@exemplo.com
MAIL_CC=copia1@exemplo.com,copia2@exemplo.com


Observação: renomeie .env.example para .env localmente e preencha os valores reais no seu ambiente de desenvolvimento. Nunca suba .env para repositório público.

Exemplo de .gitignore 
# Python
__pycache__/
*.pyc
.venv/

# Config local 
.env

# IDEs / editores
.vscode/
.idea/

Como configurar (passo a passo)

Crie um arquivo .env a partir de .env.example:

cp .env.example .env
# ou manualmente


Abra .env e preencha:

INVERTEXTO_TOKEN → token obtido em invertexto.com

SMTP_USER / SMTP_PASS → credenciais do seu provedor (para Gmail, prefira App Password)

MAIL_TO e MAIL_CC → destinatários (separados por vírgula para MAIL_CC)

USE_SSL → 1 se estiver usando porta SSL (465), 0 para STARTTLS (587)

Verifique .gitignore contém .env.

Uso (com .env)

Gerar dados (exemplo básico):

python shooter.py
# ou
python -c "from shooter import generate_fake; print(generate_fake(os.getenv('INVERTEXTO_TOKEN')))"


Enviar e-mail:

python sender.py
# ou, se o seu sender expõe função:
python -c "from sender import exemplo_uso_envio; exemplo_uso_envio('Corpo do e-mail')"


Os scripts (quando implementados conforme os exemplos) usam python-dotenv para carregar .env automaticamente no sender.py e/ou shooter.py.

Observações sobre as variáveis

USE_SSL: use 1 (true) se for conectar usando SSL direto (porta 465); use 0 para STARTTLS (porta 587).

MAIL_TO: separe múltiplos destinatários por vírgula (ou use apenas um endereço).

MAIL_CC: deixe em branco se não houver cópias. O código deve tratar strings vazias convertendo para lista vazia.

# Boas práticas de segurança

Use App Passwords quando disponível (Gmail, etc.) em vez da senha principal.

Nunca comite .env nem credenciais nos commits.

Use contas de teste para experimentos (contas temporárias ou secundárias).

Solução de problemas rápida

Erro de autenticação SMTP: verifique SMTP_USER, SMTP_PASS, porta e USE_SSL. Para Gmail, confirme App Password e que o login por app está permitido.

Timeout/API: valide INVERTEXTO_TOKEN e conectividade de rede.

E-mails em spam: envie com menos frequência, teste com outros provedores, configure SPF/DKIM se usar domínio próprio.

Contribuições

PRs e issues são bem-vindos! 
Caso tenha alguma contribuição em mente, não hesite em dar um fork e compartilha-la comigo🤝!
