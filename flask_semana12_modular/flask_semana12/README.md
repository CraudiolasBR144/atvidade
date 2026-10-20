# Semana 12 — Aplicação Flask modular

## Estrutura

- `run.py`: inicialização da aplicação.
- `app/__init__.py`: configuração da aplicação e extensões.
- `app/models.py`: tabelas do banco de dados.
- `app/forms.py`: formulário de cadastro.
- `app/routes.py`: rotas e regras da aplicação.
- `app/email_service.py`: envio pelo Mailgun e registro dos envios.
- `app/templates/`: páginas HTML.
- `.env.example`: modelo das variáveis de ambiente.

## Como executar localmente

1. Instale Python 3.10 ou superior.
2. Crie e ative um ambiente virtual:
   - Windows: `py -m venv .venv` e `.venv\\Scripts\\activate`
   - macOS/Linux: `python3 -m venv .venv` e `source .venv/bin/activate`
3. Instale as dependências: `pip install -r requirements.txt`
4. Copie `.env.example` para `.env` e preencha os dados reais do Mailgun e do aluno.
5. Inicialize o banco:
   `flask --app run.py shell`
   e, no shell, execute:
   `from app import db, create_app`
   `app = create_app()`
   `with app.app_context(): db.create_all()`
   `exit()`
6. Inicie a aplicação: `flask --app run.py run --debug`
7. Acesse `http://127.0.0.1:5000`.

## Envio de e-mail

Cada novo cadastro tenta enviar dois e-mails separados:
- para `flaskaulasweb@zohomail.com`;
- para o endereço configurado em `ALUNO_EMAIL`.

O nome e o prontuário incluídos no corpo vêm de `ALUNO_NOME` e `ALUNO_PRONTUARIO`.
O histórico registra cada envio que o Mailgun confirmou.

## PythonAnywhere

- Envie os arquivos do projeto para a sua área de arquivos.
- Crie o ambiente virtual e instale `requirements.txt`.
- Configure as variáveis do `.env` (ou as variáveis no ambiente da aplicação WSGI).
- Configure o arquivo WSGI para importar `app` de `run.py` ou, de forma equivalente, criar a aplicação com `from app import create_app; application = create_app()`.
- Reinicie a aplicação pelo painel Web do PythonAnywhere.

## Segurança

Não publique o `.env`, não envie sua chave de API ao repositório e não use `debug=True` em produção.
Se uma chave real foi compartilhada em local público, revogue-a e gere outra no painel do Mailgun.
