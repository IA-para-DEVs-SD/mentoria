# 🎯 Mentoria.IA

> Plataforma de mentoria de carreira impulsionada por inteligência artificial. Analisa seu perfil profissional, identifica gaps de competência e gera planos de desenvolvimento personalizados com ações concretas para alcançar seus objetivos.

---

## 📚 Sumário de Documentações

| Documento | Descrição |
|---|---|
| [Requisitos do Produto (PRD)](backend/docs/PRD.md) | User stories, critérios de aceite, casos de uso e requisitos não-funcionais |
| [Arquitetura do Backend](backend/docs/ARCHITECTURE.md) | Arquitetura completa: modelo de dados, endpoints, agentes IA, infraestrutura Docker |
| [Arquitetura do Frontend](frontend/docs/ARCHITECTURE.md) | Stack, estrutura de pastas, rotas, stores, fluxo do usuário |
---

## 🛠️ Tecnologias Utilizadas

| Camada | Tecnologia | Justificativa |
|---|---|---|
| Frontend | Vue.js 3 + PrimeVue 4 + Tailwind CSS 4 | Composition API, componentes enterprise-ready, utilitários CSS |
| State | Pinia | State management reativo e type-safe para Vue 3 |
| Build | Vite 7 + TypeScript 5.9 | Build rápido, HMR, tipagem forte end-to-end |
| Backend | Python 3.12 + FastAPI | Alta performance async, tipagem forte, ecossistema IA |
| ORM | SQLAlchemy + Alembic | ORM maduro com migrations versionadas |
| Banco de Dados | SQLite | Leve, sem dependências externas, ideal para MVP |
| LLM | Google Gemini 2.5 Flash via PydanticAI | Outputs estruturados com validação, agentes inteligentes |
| Autenticação | Google OAuth 2.0 + JWT (python-jose) | Login social sem senha, tokens stateless |
| Infra | Docker Compose | Frontend e backend containerizados em rede local |

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
DATABASE_URL=sqlite:///./mentoria.db
JWT_SECRET=sua-chave-secreta
GOOGLE_CLIENT_ID=seu-client-id
GOOGLE_CLIENT_SECRET=seu-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback
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
