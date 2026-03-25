# 🎯 Mentoria.IA

> Plataforma de mentoria de carreira impulsionada por inteligência artificial. Analisa seu perfil profissional, identifica gaps de competência e gera planos de desenvolvimento personalizados com ações concretas para alcançar seus objetivos.

---

## 📚 Sumário de Documentações

| Documento | Descrição |
|---|---|
| [Requisitos do Produto (PRD)](backend/docs/Requisitos.md) | User stories, critérios de aceite, casos de uso e requisitos não-funcionais |
| [Arquitetura do Sistema](backend/docs/ARCHITECTURE.md) | Decisões arquiteturais, fluxo de dados, infraestrutura e agentes de IA |
| [Prompts do Sistema](backend/docs/Prompts.md) | Versão inicial dos prompts utilizados no projeto MentorIA |
---

## 🛠️ Tecnologias Utilizadas

| Camada | Tecnologia | Justificativa |
|---|---|---|
| Frontend | Vue.js 3 + PrimeVue | Componentização rica, UI profissional e responsiva |
| Backend | Python + FastAPI | Alta performance async, tipagem forte, ecossistema IA |
| LLM | Google Gemini via PydanticAI | Outputs estruturados com validação, agentes inteligentes |
| Banco de Dados | PostgreSQL | Dados relacionais, perfis, histórico de planos |
| Cache | Redis | Sessões, cache de respostas da LLM, rate limiting |
| Infra | Docker Compose | Todos os serviços containerizados em ambiente único |
| CI/CD | GitHub Actions | Automação de deploy integrada ao repositório |

---

## 🚀 Instruções de Instalação e Uso

### Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) e [Docker Compose](https://docs.docker.com/compose/install/)
- Chave de API do [Google Gemini](https://ai.google.dev/)
- Credenciais OAuth do Google (para autenticação)

### Configuração

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/mentoria-ia.git
cd mentoria-ia
```

2. Copie o arquivo de variáveis de ambiente e preencha com suas credenciais:

```bash
cp backend/.env.example backend/.env
```

```env
GEMINI_API_KEY=sua-chave-gemini
DATABASE_URL=postgresql://user:pass@postgres:5432/mentoria
REDIS_URL=redis://redis:6379
JWT_SECRET=sua-chave-secreta
GOOGLE_CLIENT_ID=seu-client-id
GOOGLE_CLIENT_SECRET=seu-client-secret
```

3. Suba os serviços:

```bash
docker compose up -d
```

4. Acesse a aplicação:

| Serviço | URL |
|---|---|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| Documentação da API | http://localhost:8000/docs |

---

## 👥 Integrantes do Grupo

| Nome | Papel |
|---|---|
| Willian Silvano Maira | 🎵 Bardo |
| Taiane Baldin | 🛡️ Paladina |
| Murilo Henrique da Silva Pires | 🔮 Mago |
| Murilo Barcelos Corrêa | 🔮 Mago |
| Paulo Sérgio Nunes Gonçalves | 🔮 Mago |

---

## 📄 Licença

MIT
