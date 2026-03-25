# Como rodar o projeto

## Primeira vez

```bash
# 1. Criar e ativar o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Criar o .env
cp .env.example .env
```

Editar o `.env` e preencher:
- `GOOGLE_CLIENT_ID` e `GOOGLE_CLIENT_SECRET` — obtidos no [Google Cloud Console](https://console.cloud.google.com) → APIs & Services → Credentials
- `GEMINI_API_KEY` — obtida no [Google AI Studio](https://aistudio.google.com)
- `JWT_SECRET` — qualquer string longa e aleatória

```bash
# 4. Criar as tabelas no banco
alembic upgrade head

# 5. Subir o servidor
uvicorn app.main:app --reload
```

## Próximas vezes

```bash
source .venv/bin/activate
uvicorn app.main:app --reload
```

## Acessar

- Swagger UI: http://127.0.0.1:8000/docs
- Login Google: http://127.0.0.1:8000/auth/google/login
